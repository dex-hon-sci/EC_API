#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:00:18 2026

@author: dexter
"""
import asyncio
import pytest
from EC_API.connect.cqg.base import ConnectCQG
from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_streams_CQG import dummy_mixed_full_stream

    
@pytest.mark.asyncio
async def test_router_loop_mix_msg_stream():
    conn = ConnectCQG(
        host_name = "",
        user_name = "", 
        password = "",
        immediate_connect=False,
        client=object()
        )
    
    fake = FakeTransport()
    conn._transport = fake
    
    # Simulate endpoints usage of stream+message routers
    q_contract_id0 = conn._market_data_stream_router.subscribe(0)
    q_contract_id1 = conn._market_data_stream_router.subscribe(1)
    q_contract_id2 = conn._market_data_stream_router.subscribe(2)
    q_ex = conn._exec_stream_router.subscribe("order_1")
    
    conn.start()
    
    # Msg builders---
    
    # -- Router Loop tests---
    task = asyncio.create_task(conn._router_loop())

    #await fake.in_q.put(msg_md1)
    #await fake.in_q.put(msg_rpc)
    #await fake.in_q.put(msg_exec)
    #await fake.in_q.put(msg_md2)