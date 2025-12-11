#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 10 00:42:15 2025

@author: dexter
"""
import queue
import threading
import asyncio
import os
from dotenv import load_dotenv


import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.router import extract_request_id

load_dotenv()
CQG_host_url = os.getenv("CQG_API_host_name_live")
CQG_live_data_acc = os.getenv("CQG_API_data_live_usrname")
CQG_live_data_pw = os.getenv("CQG_API_data_live_pw")
CQG_live_data_privatelabel = os.getenv("CQG_API_data_live_private_label")
CQG_live_data_client_app_id = os.getenv("CQG_API_data_live_client_app_id")

# Send - not blocking
# Send - enqueue, io_loop pick up and send
# send -
# Recv - Does await transport.recv() not call any blocking CQG API directly?
# Recv - during await, can other async task still run
# Recv - recieve in order

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
        
# --- Send operations -------------
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
    print(transport.raw_client)
    transport.connect()
    transport.start()
    
    print("thread list", threading.enumerate())

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

    await transport.send(msg1) # test send
    await asyncio.sleep(0.1) # Give IO thread a moment to run
    await transport.send(msg2)
    await asyncio.sleep(0.1) 
    await transport.send(msg3)
    await asyncio.sleep(0.1) 

    # check if the send_client_message was called
    print("fk_msgs", fake_client.sent_messages)
    label_1 = fake_client.sent_messages[0].logon.private_label
    assert label_1 == "test_send_forwards_1"
    label_2 = fake_client.sent_messages[1].logon.private_label
    assert label_2 == "test_send_forwards_2"
    label_3 = fake_client.sent_messages[2].logon.private_label
    assert label_3 == "test_send_forwards_3"
    transport.stop()
    
# --- Recv operations -------------


#asyncio.run(test_transport_send2queue())

#--- Life cycle -------------------
@pytest.mark.asyncio
async def test_transport_lifecycle() -> None:
    # Lifecycle - After connect() and start(), is one IO thread running?
    # Lifecycle - After stop(), does that IO thread exit?
    # Lifecycle - Is the CQG client disconnected cleanly?

    # test if Transport can start and stop
    loop = asyncio.get_running_loop()
    transport = TransportCQG(
        host_name="demo_host",
        loop=loop,
        client=FakeCQGClient()
    )
    print(transport.raw_client)

    transport.connect()
    transport.start()
    #print('out2',threading.enumerate())
    assert len(threading.enumerate()) == 3
    #print(threading.enumerate()[1].__dict__)
    assert '_send_loop' in threading.enumerate()[1]._name
    assert '_recv_loop' in threading.enumerate()[2]._name
    transport.stop()
    await asyncio.sleep(2.0)
    #print('out3',threading.enumerate()) 
    assert len(threading.enumerate()) == 1
     

# test for non-blocking operations

# =============================================================================
# @pytest.mark.asyncio
# async def test_transport_send2queue():
#     loop = asyncio.get_running_loop()
#     fake_client = FakeCQGClient()
#     transport = TransportCQG(
#         host_name="demo_host",
#         loop=loop,
#         client=fake_client,  
#     )
# 
#     #transport.connect()
#     transport.start()
#     
#     print(threading.enumerate())
# 
#     # Build a dummy client message (no real fields needed for this test)
#     msg = ClientMsg()
#     msg.logon.user_name = "TEST"
#     msg.logon.private_label = "test_send_forwards"
# 
#     await transport.send(msg) # test s
# 
#     # Give IO thread a moment to run
#     await asyncio.sleep(0.05)
#     print("fk_msgs", fake_client.sent_messages,"msg", msg)
#     label = transport._out_q.get_nowait().logon.private_label
#     #print(type(transport._out_q.get_nowait().logon.private_label))
#     assert label == "test_send_forwards"
# 
# 
#     transport.stop()
#     #assert fake_client.disconnected
#     
# @pytest.mark.asyncio
# async def test_transport_recv2async_queue():
#     pass    
# =============================================================================
    
# sending message in the right queue,

# receving message in the right 


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