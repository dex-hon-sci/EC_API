#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 18:05:32 2026

@author: dexter
"""

import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState, CONNECT_STATES_LIFECYCLE
from EC_API.utility.state_mgr import StateMgr
#from EC_API.exceptions import 
from tests.unit.fixtures.proxy_clients import (FakeCQGClient, FakeTransport)

# --- Happy Paths: start()/stop() ---
@pytest.mark.asyncio    
async def test_connect_start_valid_disconnect_back_to_reconnecting_success() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()

    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport

        )
    state_mgr = StateMgr( 
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.DISCONNECTED, 
            cur = ConnectionState.DISCONNECTED, 
            allowed_starts=[ConnectionState.DISCONNECTED],
            ) 
    
    conn._state_mgr = state_mgr
    result = conn.start()
    assert result == True
    assert conn.state == ConnectionState.CONNECTED_DEFAULT
    await conn.stop()
    
# --- Sad Paths: start()/stop() ---
@pytest.mark.asyncio
async def test_connect_start_invalid_starting_state() -> None:
    fake_client = FakeCQGClient()
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client
        )
    state_mgr = StateMgr( 
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.CONNECTED_LOGOFF, 
            cur = ConnectionState.CONNECTED_LOGOFF, 
            allowed_starts=[ConnectionState.CONNECTED_LOGOFF] 
            ) 
    
    conn._state_mgr = state_mgr
    result = conn.start()
    assert result == False
        
@pytest.mark.asyncio    
async def test_connect_start_invalid_connect_failed() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    fake_transport.fail_connect = True
    
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport
        )
    state_mgr = StateMgr(  # Invalid state to start
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.DISCONNECTED, 
            cur = ConnectionState.DISCONNECTED, 
            allowed_starts=[ConnectionState.DISCONNECTED],
            ) 
    
    conn._state_mgr = state_mgr
    result = conn.start()
    assert result == False
    assert conn.state == ConnectionState.DISCONNECTED
    await conn.stop()
    
@pytest.mark.asyncio    
async def test_connect_stop_invalid_starting_state() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    
    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport
        )
    state_mgr = StateMgr( # Invalid state to stop
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.UNKNOWN, 
            cur = ConnectionState.UNKNOWN, 
            allowed_starts=[ConnectionState.UNKNOWN],
            ) 
    
    conn._state_mgr = state_mgr
    result = await conn.stop()
    assert result == False
    
@pytest.mark.asyncio    
async def test_connect_stop_invalid_disconnect_failed() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    fake_transport.fail_disconnect = True

    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport
        )
    state_mgr = StateMgr( # Valid state to stop
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.CONNECTED_LOGOFF, 
            cur = ConnectionState.CONNECTED_LOGOFF, 
            allowed_starts=[ConnectionState.CONNECTED_LOGOFF],
            ) 
    
    conn._state_mgr = state_mgr
    result = await conn.stop()
    assert result == False
    
@pytest.mark.asyncio    
async def test_connect_stop_invalid_stop_failed() -> None:
    fake_client = FakeCQGClient()
    fake_transport = FakeTransport()
    fake_transport.fail_stop = True

    conn = ConnectCQG(
        "host_name", "user_name", "password", 
        client = fake_client,
        transport = fake_transport
        )
    state_mgr = StateMgr( # Invalid state to stop
            CONNECT_STATES_LIFECYCLE, 
            start = ConnectionState.CONNECTED_LOGOFF, 
            cur = ConnectionState.CONNECTED_LOGOFF, 
            allowed_starts=[ConnectionState.CONNECTED_LOGOFF],
            ) 
    conn._state_mgr = state_mgr
    result = await conn.stop()
    assert result == False