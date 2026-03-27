#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:00:18 2026

@author: dexter
"""
import asyncio
import pytest
import time
from typing import Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.transport.routers import StreamRouter, MessageRouter
from EC_API.protocol.cqg.key_extractors import extractors
from EC_API.protocol.cqg.router_util import (
    extract_router_keys, server_msg_type,
    realtime_tick_contract_id
    )
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_streams_CQG import (
    dummy_realtime_data_stream,
    dummy_mixed_full_stream
    )


async def _drain_all_stream_data(
        queues: dict[int, asyncio.Queue],
        msg_stream: list[ServerMsg],
        id_func: Callable[[ServerMsg], int|str]
        ) -> None:
    # Can be used to test StreamRouter and MessageRouter.
    expected = dict()
    
    # Put the msg inside an dict by ID
    for msg in msg_stream:
        rid = id_func(msg)      
        expected.setdefault(rid,[]).append(msg)
        
    #
    for rid, msgs in expected.items():
        q = queues[rid]
        
        for expected_msg in msgs:
            received = await q.get()
            assert id_func(received) == id_func(expected_msg)
        
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
    total_msg_number = 20_000
    # Insert a Fake transport layer to siulate send/recv
    fake_transport = FakeTransport()    
    conn._transport = fake_transport

    # Put these msg_stream into the router loop
    msg_stream = dummy_realtime_data_stream(total_msg_number=total_msg_number)
    
    start = time.perf_counter()
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
    #await fake_transport.in_q.put(None)  # sentinel to signal end of stream
    elapsed = time.perf_counter() - start
    print(f"Feed time: {elapsed:4f}s")

    stream_router = StreamRouter(
        max_queue_size=100,
        max_sub_size=4,
        max_num_sym=100,
        )
    conn._mkt_data_stream_router = stream_router
    
    # Subscirbe to symbol contract_id
    contract_ids = {m.real_time_market_data[0].contract_id for m in msg_stream}
    queues = {cid: stream_router.subscribe(cid) for cid in contract_ids}
    
    # Function call transport and call send/recv loop
    conn.start()
    start = time.perf_counter()
    
    try:
        await asyncio.wait_for(_drain_all_stream_data(
            queues, msg_stream, realtime_tick_contract_id
            ), 
            timeout = 1)
    except asyncio.TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")

        pytest.fail("Asyncio Time out")
    
    await conn.stop()
  

    
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
    
    #q_ex = conn._exec_stream_router.subscribe("order_1")
    
    # Function call transport and call send/recv loop
    #conn.start()
    
    #for i in range(len()):
    ##print("msgRouter", conn._msg_router._pending)
    ##print("Mkt_stream",conn._mkt_data_stream_router._subs)
    ##print('exec_Stream', conn._exec_stream_router._subs)
    ##print('misc', conn._misc_queue)
    
    ##assert 1 ==0
    #print(list(fake.in_q._queue))
