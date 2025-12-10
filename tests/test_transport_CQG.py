#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 00:42:15 2025

@author: dexter
"""
import queue
import threading
import asyncio
import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.router import extract_request_id
# Fakeclient


class FakeCQGClient:
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
        
        
# Life cycle
# transport.start()
async def test_transport_lifecycle():
    pass

# test for non-blocking operations

@pytest.mark.asyncio
async def test_transport_send2queue():
    loop = asyncio.get_running_loop()
    fake_client = FakeCQGClient()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=fake_client,  
    )

    #transport.connect()
    transport.start()
    
    print(threading.enumerate())

    # Build a dummy client message (no real fields needed for this test)
    msg = ClientMsg()
    msg.logon.user_name = "TEST"
    msg.logon.private_label = "test_send_forwards"

    await transport.send(msg) # test s

    # Give IO thread a moment to run
    await asyncio.sleep(0.05)
    print("fk_msgs", fake_client.sent_messages,"msg", msg)
    label = transport._out_q.get_nowait().logon.private_label
    #print(type(transport._out_q.get_nowait().logon.private_label))
    assert label == "test_send_forwards"


    transport.stop()
    #assert fake_client.disconnected
    
@pytest.mark.asyncio
async def test_transport_recv2async_queue():
    pass    
    
# sending message in the right queue,

# receving message in the right 

#asyncio.run(test_send_forwards_to_client())

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
            
# Message Construction
# Message Transport send()
# Message Transport recv()
# Message Router Transform to Futures