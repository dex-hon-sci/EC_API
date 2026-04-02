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
from EC_API._typing import RouterKey
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.transport.routers import StreamRouter, MessageRouter
from EC_API.protocol.cqg.router_util import (
    extract_router_keys, server_msg_type,
    realtime_tick_contract_id,
    order_statuses_order_id,
    split_server_msg
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
    dummy_composite_mkt_data_stream,
    dummy_composite_order_statuses_stream,
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
    await asyncio.sleep(0.1)

    for fut, msg, key in zip(futs, msg_stream, keys):
        assert fut.done()
        assert fut.result() is msg
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
    
    order_reqest_reject_fut = msg_router.register_key(order_reqest_reject_key)
    order_reqest_acks_fut = msg_router.register_key(order_reqest_acks_key)
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
        assert fut.result() is msg
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
    # Assume extract_router_keys() is well tested
    # Assume each msg has only one key in this case.
    all_keys = [extract_router_keys(msg)[0] for msg in msg_stream]
    all_futs = [msg_router.register_key(key) for key in all_keys]
    
    # Start the test
    conn.start()
    await asyncio.sleep(0.1)

    for msg, key, fut in zip(msg_stream, all_keys, all_futs):
        assert fut.done()
        assert fut.result() is msg
        assert key not in conn._msg_router.pending
    await conn.stop()
    
    
@pytest.mark.asyncio
async def test_router_loop_composite_msg() -> None:
    num_comp_mkt_data = 5
    num_order_statuses = 5
    # sub, 
    conn = ConnectCQG(
        host_name = "",
        user_name = "",     
        password = "",
        immediate_connect=False,
        client=object()
        )

    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    msg_stream_comp_mkt_data = dummy_composite_mkt_data_stream(num=num_comp_mkt_data)
    msg_stream_comp_ord_statuses = dummy_composite_order_statuses_stream(num=num_order_statuses)
    
    # Separate rpc msg and stream msg into two list for answer matching later
    mkt_targets = ['market_data_subscription_statuses', 'real_time_market_data']
    order_targets = ['order_request_acks', 'trade_subscription_statuses',
                     'trade_snapshot_completions','order_statuses']

    msg_stream_comp_mkt_data_rpc = [
        split_server_msg(msg, mkt_targets)[0] 
        for i, msg in enumerate(msg_stream_comp_mkt_data)]
    msg_stream_comp_mkt_data_stream = [
        split_server_msg(msg, mkt_targets)[1]
        for i, msg in enumerate(msg_stream_comp_mkt_data)]
    
    #msg_stream_comp_mkt_data_stream = []
    #for i, msg in enumerate(msg_stream_comp_mkt_data):
    #    S = split_server_msg(msg, mkt_targets)
    #    msg_stream_comp_mkt_data_stream.append(S[0])
    #    msg_stream_comp_mkt_data_stream.append(S[1])
        
    
    msg_stream_comp_ord_statuses_rpc = []
    for i, msg in enumerate(msg_stream_comp_ord_statuses):
        q = split_server_msg(msg, order_targets)
        msg_stream_comp_ord_statuses_rpc.append(q[0])
        msg_stream_comp_ord_statuses_rpc.append(q[1])
        msg_stream_comp_ord_statuses_rpc.append(q[2])
        
    msg_stream_comp_ord_statuses_stream = [
        split_server_msg(msg, order_targets)[3] 
        for i, msg in enumerate(msg_stream_comp_ord_statuses)]
        
    # Put the two message streams in the fake transport client
    start = time.perf_counter()
    for msg1, msg2 in zip(msg_stream_comp_mkt_data, msg_stream_comp_ord_statuses):
        await fake_transport.in_q.put(msg1)
        await fake_transport.in_q.put(msg2)
    elapsed = time.perf_counter() - start
    
    # Define MessageRouter+StreamRouter, put it in the Connect object
    conn._msg_router = MessageRouter()
    conn._exec_stream_router =  StreamRouter()
    conn._mkt_data_stream_router =  StreamRouter()

    # For keys and fut for rpc-like, sub-like msg types
    def _build_key_answers_order_statuses() -> list[RouterKey]:
        rpc_keys = []
        for i in range(num_order_statuses):
            rpc_keys.append(('rpc_reqid', 'order_request_acks', 'request_id', i*10 + 0))
            rpc_keys.append(('sub', 'trade_subscription_statuses', 'id', i*10 + 1))
            rpc_keys.append(('sub', 'trade_snapshot_completions', 'subscription_id', i*10 + 2))
        return rpc_keys
    
    
    def _build_key_answers_mkt_data() -> list[RouterKey]:
        mkt_keys = []
        for i in range(num_comp_mkt_data):
            mkt_keys.append(('md', 'market_data_subscription_statuses', 'contract_id',  i*10 + 0))
            mkt_keys.append(('md', 'real_time_market_data', 'contract_id',  i*10 + 1))
        return mkt_keys
    

    # For keys and fut for substream msg types
    rpc_keys = _build_key_answers_order_statuses()
    rpc_futs = [conn._msg_router.register_key(key) for key in rpc_keys]
    
    # Subscribe to the right chain_order_id for order status
    print('msg_stream_comp_ord_statuses_stream', len(msg_stream_comp_ord_statuses_stream))
    for m in msg_stream_comp_ord_statuses_stream:
        print(m.order_statuses)
    chain_order_ids = {m.order_statuses[0].chain_order_id for m in msg_stream_comp_ord_statuses_stream}
    queues = {cid: conn._exec_stream_router.subscribe(cid) for cid in chain_order_ids}

    # Subscribe to the right contract_ids for real time data
    contract_ids = {m.real_time_market_data[0].contract_id for m in msg_stream_comp_mkt_data_stream}
    queues_mkt = {cid: conn._mkt_data_stream_router.subscribe(cid) for cid in contract_ids}

    # start the test
    conn.start()
    await asyncio.sleep(0.1)

    # Check RPC message. Both Trade session and Data channel uses the same
    # MessageRouter
    for msg, key, fut in zip(msg_stream_comp_ord_statuses_rpc, rpc_keys, rpc_futs):
        assert fut.done()
        assert key not in conn._msg_router.pending
        assert fut.result() == msg
        
    # Check order status stream
    try:
        await asyncio.wait_for(_drain_all_stream_data(
            queues, msg_stream_comp_ord_statuses_stream, order_statuses_order_id
            ), timeout=1)
    except asyncio.TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")
        pytest.fail("Asyncio Time out")
    
    # check market data stream
    try:
        await asyncio.wait_for(_drain_all_stream_data(
            queues_mkt, msg_stream_comp_mkt_data_stream, realtime_tick_contract_id
            ), timeout=1)
    except asyncio.TimeoutError:
        elapsed = time.perf_counter() - start
        print(f"Drain time: {elapsed:.4f}s")
        pytest.fail("Asyncio Time out")
    
@pytest.mark.asyncio
async def test_router_loop_empty_msg():
    num = 10
    
    conn = ConnectCQG(
        host_name = "",
        user_name = "",     
        password = "",
        immediate_connect=False,
        client=object()
        )

    fake_transport = FakeTransport()    
    conn._transport = fake_transport
    
    msg_stream = [ServerMsg() for _ in range(num)]
    

@pytest.mark.asyncio
async def test_router_loop_transport_dies():...

