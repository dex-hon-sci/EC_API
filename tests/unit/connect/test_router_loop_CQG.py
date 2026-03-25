#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:00:18 2026

@author: dexter
"""
import asyncio
import pytest
import time
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.transport.routers import StreamRouter, MessageRouter
from EC_API.protocol.cqg.key_extractors import extractors
from EC_API.protocol.cqg.router_util import extract_router_keys, server_msg_type
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_streams_CQG import (
    dummy_realtime_data_stream,
    dummy_mixed_full_stream)

@pytest.mark.asyncio
async def test_router_loop_realtime_mkt_stream_valid() -> None:
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    
    total_contract_sub = 20
    # Insert a Fake transport layer to siulate send/recv
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    stream_router = StreamRouter(
        max_queue_size=100,
        max_sub_size=4,
        max_num_sym=20,
        )
    conn._mkt_data_stream_router = stream_router
    

    # Subscirbe to symbol contract_id
    contract_id_to_q_dict = {
        i: conn._mkt_data_stream_router.subscribe(i) 
        for i in range(total_contract_sub)
        }

    # Put these msg_stream into the router loop
    msg_stream = dummy_realtime_data_stream(total_msg_number=total_contract_sub)
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
        
    # Function call transport and call send/recv loop
    conn.start()
    await asyncio.sleep(3)
    
    # Test if the message are all accounted  
    for _ in range(len(msg_stream)):
        input_msg = msg_stream.pop()
        
        print(server_msg_type(input_msg), 'servermsgtype')

        contract_id = input_msg.real_time_market_data[0].contract_id
        if conn._mkt_data_stream_router._subs.get(contract_id):
            if len(conn._mkt_data_stream_router._subs[contract_id])>0:
                out_msg = await conn._mkt_data_stream_router._subs[contract_id][0].get()
                print('out_msg', out_msg)
                assert out_msg.real_time_market_data[0].contract_id == input_msg.real_time_market_data[0].contract_id

    await conn.stop()
    assert 1 == 0
  

    
@pytest.mark.asyncio
async def test_router_loop_orderstatus_updates_stream_valid() -> None:
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    total_contract_sub = 20

@pytest.mark.asyncio
async def test_router_loop_rpc_msg_routing_valid() -> None:
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    total_contract_sub = 20

    
@pytest.mark.asyncio
async def test_router_loop_mix_msg_stream_valid():
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    total_contract_sub = 20

    # Insert a Fake transport layer to siulate send/recv
    fake_transport = FakeTransport()    
    conn._transport = fake_transport

    # Msg builders---
    msg_stream = dummy_mixed_full_stream(seed=100)    
    router_keys = [extract_router_keys(msg) for msg in msg_stream] 
    router_keys_len = [len(key) for key in router_keys]
    #print(router_keys)
    #print(router_keys_len)
    #print(len(msg_stream)==len(router_keys))
    # -- Router Loop tests---
    task = asyncio.create_task(conn._router_loop())

    # Put these msg_stream into the router loop
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
        
    # Make corresponding router keys for each message in msg

    # Simulate endpoints usage of stream+message routers
    contract_id_to_q_dict = {
        i: conn._mkt_data_stream_router.subscribe(i) for i in range(total_contract_sub)
        }
    
    q_ex = conn._exec_stream_router.subscribe("order_1")
    
    # Function call transport and call send/recv loop
    conn.start()
    
    #for i in range(len()):
    ##print("msgRouter", conn._msg_router._pending)
    ##print("Mkt_stream",conn._mkt_data_stream_router._subs)
    ##print('exec_Stream', conn._exec_stream_router._subs)
    ##print('misc', conn._misc_queue)
    
    ##assert 1 ==0
    #print(list(fake.in_q._queue))
