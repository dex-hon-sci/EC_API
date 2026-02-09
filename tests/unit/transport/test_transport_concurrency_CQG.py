#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:03:13 2025

@author: dexter
"""
import threading
import asyncio
import time
# Python Package imports
import pytest
# EC_API imports
from EC_API.transport.cqg.base import TransportCQG
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from tests.unit.transport.proxy import FakeCQGClient

def _find_threads(prefix: str):
    return [t for t in threading.enumerate() if t.name.startswith(prefix)]

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
    print(received_ids, elapsed)
    
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
    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
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
    
    deadline = time.monotonic() + 2.0
    while _find_threads("TransportCQG") and time.monotonic() < deadline:
        await asyncio.sleep(0.01)
    assert _find_threads("TransportCQG") == []
    assert fake_client.disconnected is True
    
