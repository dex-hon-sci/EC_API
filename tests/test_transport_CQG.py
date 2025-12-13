#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 00:42:15 2025

@author: dexter
"""
# Python imports
import queue
import threading
import asyncio
import os
import time
from dotenv import load_dotenv
# Python Package imports
import pytest
# EC_API imports
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.transport.cqg.base import TransportCQG

load_dotenv()
CQG_host_url = os.getenv("CQG_API_host_name_live")
CQG_live_data_acc = os.getenv("CQG_API_data_live_usrname")
CQG_live_data_pw = os.getenv("CQG_API_data_live_pw")
CQG_live_data_privatelabel = os.getenv("CQG_API_data_live_private_label")
CQG_live_data_client_app_id = os.getenv("CQG_API_data_live_client_app_id")

class FakeCQGClient:
    # For the dependecy injection in unit tests
    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.sent_messages: list[ClientMsg] = []
        self._incoming = queue.Queue()
        
    def connect(self, host_name: str):
        self.connected = True

    def disconnect(self):
        self.disconnected = True
        # Optionally unblock receive by putting a sentinel
        self._incoming.put(None)

    def send_client_message(self, msg: ClientMsg):
        self.sent_messages.append(msg)

    def receive_server_message(self) -> ServerMsg:
        """
        Blocking read. For tests, we simulate this with queue.get().
        """
        msg = self._incoming.get()
        if msg is None:
            # Treat sentinel as "no more messages"
            raise RuntimeError("Client closed")
        return msg

    def push_incoming(self, msg: ServerMsg):
        """Helper: push a message so transport.recv() can eventually see it."""
        self._incoming.put(msg)
        
# --- Send-only operations -------------
@pytest.mark.asyncio
async def test_transport_send2queue():
    # testing send 
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,  
    )
    transport.connect()
    transport.start()
    
    # Build a dummy client message (no real fields needed for this test)
    msg1 = ClientMsg()
    msg1.logon.user_name = "TEST1"
    msg1.logon.private_label = "test_send_forwards_1"
    
    msg2 = ClientMsg()
    msg2.logon.user_name = "TEST2"
    msg2.logon.private_label = "test_send_forwards_2"
    
    msg3 = ClientMsg()
    msg3.logon.user_name = "TEST3"
    msg3.logon.private_label = "test_send_forwards_3"

    private_labels = [f"test_send_forwards_{i+1}" for i in range(3)]
        
    for i, msg in enumerate([msg1, msg2, msg3]):
        await transport.send(msg)
    
        duration = time.monotonic() + 1.0
        while len(fake_client.sent_messages) < i+1 and time.monotonic() < duration:
            await asyncio.sleep(0.01)
            
        label = fake_client.sent_messages[i].logon.private_label
        assert label == private_labels[i]
        
    transport.stop()
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while threads and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert threads == []
    assert fake_client.disconnected is True
    
# --- Recv-only operations -------------
@pytest.mark.asyncio
async def test_transport_recv2async_queue() -> None:
    # testing recieve 
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,  
    )
    transport.connect()
    transport.start()
    
    # Dummy results for testing receive functions in the transport layer
    msg1 = ServerMsg()
    msg1.logon_result.result_code = 0
    
    msg2 = ServerMsg()
    msg2.logon_result.result_code = 101
    
    msg3 = ServerMsg()
    msg3.logon_result.result_code = 102
    
    fake_client.push_incoming(msg1)
    fake_client.push_incoming(msg2)
    fake_client.push_incoming(msg3)
    
    for i, ele in enumerate([0, 101, 102]):
        recv_msg = await asyncio.wait_for(transport.recv(), timeout=1.0)            
        res_code = recv_msg.logon_result.result_code        
        assert res_code == ele

    transport.stop()
    
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while threads and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert threads == []
    assert fake_client.disconnected is True


#--- Life cycle -------------------
@pytest.mark.asyncio
async def test_transport_lifecycle() -> None:
    # Lifecycle - After connect() and start(), is one IO thread running?
    # Lifecycle - After stop(), does that IO thread exit?
    # Lifecycle - Is the CQG client disconnected cleanly?
    def _find_threads(prefix: str):
        return [t for t in threading.enumerate() if t.name.startswith(prefix)]
    
    # test if Transport can start and stop
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client
    )
    print(transport.raw_client)
    transport.connect()
    transport.start()
    print([t.name for t in threading.enumerate()])
    
    threads = _find_threads("TransportCQG")
    assert any("send_loop" in t.name for t in threads)
    assert any("recv_loop" in t.name for t in threads)
    transport.stop()

    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
    assert fake_client.disconnected is True

    
# --- Send + Recv operations -------------
@pytest.mark.asyncio
async def test_transport_concurrent_sendandrecv() -> None:
    
    N = 20
    # Test for non-blocking behaviour
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()

    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,
    )
    
    transport.connect()
    transport.start()
    
    async def sender():
        for i in range(N):
            msg = ClientMsg()
            msg.logon.user_name = f"USER_{i}"
            msg.logon.private_label = f"OUT_{i}"
            await transport.send(msg)
            # Tiny delay to interleave with receiver
            await asyncio.sleep(0.001)
    
    async def receiver() -> tuple[list, float]:
        received_ids = []
        start = time.monotonic()
        
        for _ in range(N):
            msg = await asyncio.wait_for(transport.recv(), timeout=1.0)
            received_ids.append(msg.logon_result.result_code)
        
        elapsed = time.monotonic() - start
        return received_ids, elapsed
    
    async def pusher():
        # Push messages into fake_client._incoming, which recv_loop will read
        for i in range(N):
            smsg = ServerMsg()
            smsg.logon_result.result_code = i
            fake_client.push_incoming(smsg)
            await asyncio.sleep(0.001)
    
    # Run coroutines to send and recv
    # Run them all together
    recv_task = asyncio.create_task(receiver())
    await asyncio.gather(sender(), pusher())
    received_ids, elapsed = await recv_task
    
    # 1) Check outbound hit the fake client in order
    assert len(fake_client.sent_messages) == N
    out_labels = [m.logon.private_label for m in fake_client.sent_messages]
    assert out_labels == [f"OUT_{i}" for i in range(N)]
    
    # 2) Check inbound ordering
    assert received_ids == [i for i in range(N)]
    
    # 3) Check we didn't spend "forever" waiting. This doesn't prove low latency,
    #    but it detects obvious blocking / deadlocks. Tune bound as needed.
    assert elapsed < 1.0
    
    transport.stop()
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while threads and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert threads == []
    assert fake_client.disconnected is True

@pytest.mark.asyncio
async def test_transport_shutdown_on_disconnect():
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,
    )

    # 1) Start transport
    transport.connect()
    transport.start()

    # 2) Push one incoming message: should be received normally
    from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
    msg1 = ServerMsg()
    msg1.logon_result.result_code = 0
    fake_client.push_incoming(msg1)

    got1 = await asyncio.wait_for(transport.recv(), timeout=1.0)
    assert got1.logon_result.result_code == 0

    transport.stop()
    
    threads = [t for t in threading.enumerate() if t.name.startswith("TransportCQG")]
    deadline = time.monotonic() + 2.0
    while threads and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert threads == []
    assert fake_client.disconnected is True
    


# =============================================================================
# class FakeEngine:
#     def __init__(self, host_name, loop):
#         self.host_name = host_name
#         self.loop = loop 
#         self._transport = TransportCQG(host_name)
#         self._router = None
#         
#     async def _router_loop(self):
#         while True:
#             msg = await self._transport.recv()
#             
#             if msg is not None:
#                 self._router.on_message(msg)
#                 continue
# =============================================================================
            
