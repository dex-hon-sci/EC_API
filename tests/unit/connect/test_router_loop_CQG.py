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
    realtime_tick_contract_id,
    order_statuses_order_id
    )
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_pong_server_msg,
    build_trade_subscription_statuses_server_msg,
    build_trade_snapshot_completetions_server_msg,
    build_order_statuses_server_msg,
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg

    )
from tests.unit.fixtures.server_msg_streams_CQG import (
    dummy_rpc_stream,
    dummy_session_stream,
    dummy_info_stream,
    dummy_realtime_data_stream,
    dummy_order_update_stream,
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
        
    for rid, msgs in expected.items():
        q = queues[rid]
        
        for expected_msg in msgs:
            received = await q.get()
            assert id_func(received) == id_func(expected_msg)
        
        
@pytest.mark.asyncio
async def test_bench_stream_router_publish() -> None:
    N = 10_000
    msg_stream = dummy_realtime_data_stream(total_msg_number=N)
    
    router = StreamRouter(max_queue_size=N, max_sub_size=4, max_num_sym=100)
    contract_ids = {m.real_time_market_data[0].contract_id for m in msg_stream}
    for cid in contract_ids:
        router.subscribe(cid)
    
    start = time.perf_counter()
    for msg in msg_stream:
        cid = msg.real_time_market_data[0].contract_id
        await router.publish(cid, msg)
    elapsed = time.perf_counter() - start
    
    print(f"router.publish: {N/elapsed:,.0f} msg/s  |  {elapsed/N*1e6:.2f} µs/msg")
    
@pytest.mark.asyncio
async def test_starvation_check() -> None:
    N = 10_000
    msg_stream = dummy_realtime_data_stream(total_msg_number=N)
    
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    fake_transport = FakeTransport()
    conn._transport = fake_transport

    stream_router = StreamRouter(
        max_queue_size=10000,
        max_sub_size=4,
        max_num_sym=100,
        )
    conn._mkt_data_stream_router = stream_router

    # pre-fill transport queue
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
        
    contract_ids = {m.real_time_market_data[0].contract_id for m in msg_stream}
    queues = {cid: stream_router.subscribe(cid) for cid in contract_ids}
        
    expected = dict()
    
    # Put the msg inside an dict by ID
    for msg in msg_stream:
        rid = realtime_tick_contract_id(msg)      
        expected.setdefault(rid,[]).append(msg)

    # start test
    conn.start()
    
    # give router_loop a head start
    await asyncio.sleep(0)

    # check if drain_all ever gets cpu time
    drained = 0
    async def counting_drain():
        nonlocal drained
        for cid, msgs in expected.items():
            for _ in msgs:
                await queues[cid].get()
                drained += 1
                if drained % 100 == 0:
                    print(f"drained {drained} at {time.perf_counter():.4f}")
    
    await asyncio.wait_for(counting_drain(), timeout=5.0)
    
@pytest.mark.asyncio
async def test_router_loop_realtime_mkt_stream_valid() -> None:
    total_contract_sub = 20
    total_msg_number = 10_000
    # Insert a Fake transport layer to siulate send/recv
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
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
        max_queue_size=10000,
        max_sub_size=4,
        max_num_sym=100,
        )
    conn._mkt_data_stream_router = stream_router
    
    # Subscirbe to symbol contract_id
    contract_ids = {m.real_time_market_data[0].contract_id for m in msg_stream}
    queues = {cid: stream_router.subscribe(cid) for cid in contract_ids}
    
    # Function call transport and call send/recv loop
    start = time.perf_counter()
    conn.start()
    try:
        await asyncio.wait_for(_drain_all_stream_data(
            queues, msg_stream, realtime_tick_contract_id
            ), 
            timeout = 1)
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")

    except asyncio.TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")
        pytest.fail("Asyncio Time out")
    
    await conn.stop()
  
    
@pytest.mark.asyncio
async def test_router_loop_orderstatus_updates_stream_valid() -> None:
    # Insert a Fake transport layer to siulate send/recv
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    # put dummy messages in the fake transport client
    msg_stream = dummy_order_update_stream()
    
    start = time.perf_counter()
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
    #await fake_transport.in_q.put(None)  # sentinel to signal end of stream
    elapsed = time.perf_counter() - start
    print(f"Feed time: {elapsed:4f}s")
    
    # Define StreamRouter, put it in the Connect object
    stream_router = StreamRouter(
        )
    conn._exec_stream_router = stream_router
    
    # Subscirbe to symbol contract_id
    chain_order_ids = {m.order_statuses[0].chain_order_id for m in msg_stream}
    queues = {cid: stream_router.subscribe(cid) for cid in chain_order_ids}

    # start router loop
    start = time.perf_counter()
    conn.start()
    try:
        await asyncio.wait_for(_drain_all_stream_data(
            queues, msg_stream, order_statuses_order_id
            ), timeout=1)
    except asyncio.TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")
        pytest.fail("Asyncio Time out")
    
    await conn.stop()
    
@pytest.mark.asyncio
async def test_router_loop_session_msg_routing_valid():
    # Insert a Fake transport layer to siulate send/recv
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    # Put in the dummy messages
    msg_stream = dummy_session_stream(pong_number = 10)
    start = time.perf_counter()
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
    #await fake_transport.in_q.put(None)  # sentinel to signal end of stream
    elapsed = time.perf_counter() - start
    print(f"Feed time: {elapsed:4f}s")
    
    # Define MessageRouter, put it in the Connect object
    msg_router = MessageRouter()
    conn._msg_router = msg_router
    
    logon_key = ('session', 'logon_result', 'single', 0)
    logoff_key = ('session', 'logged_off', 'single', 0)
    restore_key = ('session', 'restore_or_join_session_result', 'single', 0)
    
    fut_logon = msg_router.register_key(logon_key)
    fut_restore = msg_router.register_key(restore_key)
    fut_logoff = msg_router.register_key(logoff_key)
    
    pong_futs, pong_keys = [], []
    for i in range(10):
        pong_key = ('session', 'pong', 'token', str(i))
        pong_keys.append(pong_key)
        pong_futs.append(msg_router.register_key(pong_key))
        
    
    futs = [fut_logon] + pong_futs + [fut_restore, fut_logoff]
    keys = [logon_key] + pong_keys + [restore_key, logoff_key]
    
    conn.start()
    await asyncio.sleep(0.5)

    for fut, msg, key in zip(futs, msg_stream, keys):
        assert fut.done()
        assert fut.result() == msg
        assert key not in conn._msg_router.pending
        
    await conn.stop()
    
@pytest.mark.asyncio
async def test_router_loop_rpc_msg_routing_valid() -> None:
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    # Put in the dummy messages
    msg_stream = dummy_rpc_stream()
    start = time.perf_counter()
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
    #await fake_transport.in_q.put(None)  # sentinel to signal end of stream
    elapsed = time.perf_counter() - start
    print(f"Feed time: {elapsed:4f}s")
    
    # Define MessageRouter, put it in the Connect object
    msg_router = MessageRouter()
    conn._msg_router = msg_router
    
    order_reqest_reject_key = ('rpc_reqid', 'order_request_rejects', 'request_id', 1)
    order_reqest_acks_key = ('rpc_reqid', 'order_request_acks', 'request_id', 1)
    go_flat_status_key = ('rpc_reqid', 'go_flat_statuses', 'request_id', 1)
    
    #trade_sub_status_fut = msg_router.register_key(trade_sub_status_key)
    order_reqest_reject_fut = msg_router.register_key(order_reqest_reject_key)
    order_reqest_acks_fut = msg_router.register_key(order_reqest_acks_key)
    #acc_summ_status_fut = msg_router.register_key(acc_summ_status_key)
    go_flat_status_fut = msg_router.register_key(go_flat_status_key)

    keys = [order_reqest_reject_key, 
            order_reqest_acks_key, 
            go_flat_status_key]
    futs = [order_reqest_reject_fut, 
            order_reqest_acks_fut, 
            go_flat_status_fut]
    
    conn.start()
    await asyncio.sleep(0.5)
    
    for fut, msg, key in zip(futs, msg_stream, keys):
        assert fut.done()
        assert fut.result() == msg
        assert key not in conn._msg_router.pending
        
    await conn.stop()

@pytest.mark.asyncio
async def test_router_loop_info_msg_routing_valid():
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    # Put in the dummy messages
    msg_stream = dummy_info_stream()

    start = time.perf_counter()
    for msg in msg_stream:
        await fake_transport.in_q.put(msg)
    elapsed = time.perf_counter() - start
    print(f"Feed time: {elapsed:4f}s")
    
    # Define MessageRouter, put it in the Connect object
    msg_router = MessageRouter()
    conn._msg_router = msg_router
    
    info_key_1 = (1, "CLE", "1", "A", "id_1", "CLEXXX", "id_1", "Instrument_1")
    info_key_2 = (2, "HOE", "2", "B", "id_2", "HOEXXX", "id_2", "Instrument_2")
    info_key_3 = (3, "RBE", "3", "C", "id_3", "RBEXXX", "id_3", "Instrument_3")
    info_key_4 = (4, "QO", "4", "D", "id_4", "QOXXX", "id_4", "Instrument_4")
    info_key_5 = (5, "QP", "5", "E", "id_5", "QPXXX", "id_5", "Instrument_5")
    info_key_6 = (6, "VX", "6", "F", "id_6", "VXXXX", "id_6", "Instrument_6")
    info_key_7 = (7, "AUX", "7", "G", "id_7", "AUXXXX", "id_7", "Instrument_7")
    info_key_8 = (8, "AG", "8", "H", "id_8", "AGXXX", "id_8", "Instrument_8")
    info_key_9 = (9, "VC", "9", "I", "id_9", "VCXXX", "id_9", "Instrument_9")
    info_key_10 = (10, "EUR", "10", "J", "id_10", "EURXXX", "id_10", "Instrument_10")
    info_key_11 = (11, "YU", "11", "K", "id_11", "YUXXX", "id_11", "Instrument_11")
    info_key_12 = (12, "TAR", "12", "L", "id_12", "TARXXX", "id_12", "Instrument_12")
    info_key_13 = (13, "PEQ", "13", "M", "id_13", "PEQXXX", "id_13", "Instrument_13")

    ('info', 'information_reports:symbol_resolution_report', 'id', 1)

@pytest.mark.asyncio
async def test_router_loop_composite_msg() -> None:
    # sub, 
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    total_contract_sub = 20
    
    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    

@pytest.mark.asyncio
async def test_router_loop_transport_dies():...

# =============================================================================
# @pytest.mark.asyncio
# async def test_router_loop_mix_msg_stream_valid():
#     conn = ConnectCQG(
#         host_name = "",
#         user_name = "", 
#         password = "",
#         immediate_connect=False,
#         client=object()
#         )
#     total_contract_sub = 20
# 
#     # Insert a Fake transport layer to siulate send/recv
#     fake_transport = FakeTransport()    
#     conn._transport = fake_transport
# 
#     # Msg builders---
#     msg_stream = dummy_mixed_full_stream(seed=100)    
#     router_keys = [extract_router_keys(msg) for msg in msg_stream] 
#     router_keys_len = [len(key) for key in router_keys]
#     # -- Router Loop tests---
#     task = asyncio.create_task(conn._router_loop())
# 
#     # Put these msg_stream into the router loop
#     for msg in msg_stream:
#         await fake_transport.in_q.put(msg)
#         
#     # Make corresponding router keys for each message in msg
# 
#     # Simulate endpoints usage of stream+message routers
#     contract_id_to_q_dict = {
#         i: conn._mkt_data_stream_router.subscribe(i) for i in range(total_contract_sub)
#         }
#     
#     #q_ex = conn._exec_stream_router.subscribe("order_1")
#     
#     # Function call transport and call send/recv loop
#     #conn.start()
#     
#     #for i in range(len()):
#     ##print("msgRouter", conn._msg_router._pending)
#     ##print("Mkt_stream",conn._mkt_data_stream_router._subs)
#     ##print('exec_Stream', conn._exec_stream_router._subs)
#     ##print('misc', conn._misc_queue)
#     
#     ##assert 1 ==0
#     #print(list(fake.in_q._queue))
# =============================================================================
