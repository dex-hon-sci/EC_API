#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 16:09:18 2026

@author: dexter
"""
import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from tests.unit.fixtures.proxy_clients import (FakeCQGClient, FakeTransport)

@pytest.mark.asyncio
async def test_connect_client_property() -> None:
    fake_client = FakeCQGClient()
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client
        )
    
    assert isinstance(conn.client, FakeCQGClient)
    
@pytest.mark.asyncio
async def test_connect_immediate_connect_True() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport,
        immediate_connect= True
        )
    assert conn.state == ConnectionState.CONNECTED_DEFAULT
    await conn.stop()
    
@pytest.mark.asyncio
async def test_rid_exceed_max_limit() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport,
        immediate_connect= True
        )
    conn._rid = 2_000_000_000
    # Next request ID is 1
    assert conn.rid() == 1
    