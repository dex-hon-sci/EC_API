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
from EC_API.exceptions import (
    ConnectEnterError, 
    TransportDisconnectError
    )
from tests.unit.fixtures.proxy_clients import (
    FakeCQGClient, 
    FakeTransport
    )

# --- Happy Paths: __del__ ---

# --- Happy Paths: aenter/aexit ---
@pytest.mark.asyncio    
async def test_context_manager_normal_enter_exit_valid() -> None:
    fake_transport = FakeTransport()
    async with ConnectCQG(
        "host", "user", "pass",
        client=FakeCQGClient(),
        transport=fake_transport
    ) as conn:
        # __aenter__ ran start(), so we should be connected
        assert isinstance(conn, ConnectCQG)
        assert conn.state == ConnectionState.CONNECTED_DEFAULT

    # __aexit__ ran stop(), so connection should be fully torn down
    assert conn.state == ConnectionState.CLOSED
    
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
    

# --- Sad Paths: __del__ ---

# --- Sad Paths: aenter/aexit ---
@pytest.mark.asyncio
async def test_context_manager_cleans_up_on_exception() -> None:
    fake_transport = FakeTransport()
    with pytest.raises(ConnectEnterError):
        async with ConnectCQG(
            "host", "user", "pass",
            client=FakeCQGClient(),
            transport=fake_transport
        ) as conn:
            raise ConnectEnterError("something went wrong")

    # __aexit__ should have called stop() despite the exception
    assert conn.state == ConnectionState.CLOSED
    
@pytest.mark.asyncio
async def test_context_manager_raises_when_start_fails() -> None:
    fake_transport = FakeTransport()
    fake_transport.fail_connect = True

    with pytest.raises(ConnectEnterError):
        async with ConnectCQG(
            "host", "user", "pass",
            client=FakeCQGClient(),
            transport=fake_transport
            ):
            pass
    
# Branch 1 — already in terminal state, stop() should NOT be called
@pytest.mark.asyncio
async def test_aexit_skips_stop_when_already_closed() -> None:
    fake_transport = FakeTransport()
    async with ConnectCQG(
        "host", "user", "pass",
        client=FakeCQGClient(),
        transport=fake_transport
    ) as conn:
        await conn.stop()  # manually stop inside the block
        assert conn.state == ConnectionState.CLOSED
        # __aexit__ will now see CLOSED state and skip stop()

    # state unchanged — stop() was not called a second time
    assert conn.state == ConnectionState.CLOSED


# Branch 2 implicit — exceptions are never suppressed
@pytest.mark.asyncio
async def test_aexit_does_not_suppress_exceptions() -> None:
    fake_transport = FakeTransport()
    with pytest.raises(RuntimeError, match="boom"):
        async with ConnectCQG(
            "host", "user", "pass",
            client=FakeCQGClient(),
            transport=fake_transport
        ) as conn:
            raise RuntimeError("boom")
    # exception propagated — aexit returned False


# Branch 3 — stop() fails (transport.disconnect raises)
@pytest.mark.asyncio
async def test_aexit_handles_stop_failure() -> None:
    fake_transport = FakeTransport()

    def failing_disconnect():
        raise TransportDisconnectError("socket gone")

    fake_transport.disconnect = failing_disconnect

    async with ConnectCQG(
        "host", "user", "pass",
        client=FakeCQGClient(),
        transport=fake_transport
    ) as conn:
        pass  # __aexit__ will call stop(), which will fail

    # should not raise — aexit catches the failure and returns False
    assert conn.state != ConnectionState.CLOSED    
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
