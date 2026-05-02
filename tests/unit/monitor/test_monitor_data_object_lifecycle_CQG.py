#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:20:21 2026

@author: dexter
"""

import pytest
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from tests.unit.fixtures.proxy_clients import FakeTransport, FakeCQGClient

# --- Happy Paths aenter/aexit
@pytest.mark.asyncio
async def test_context_manager_normal_enter_exit_valid() -> None:
    conn = ConnectCQG(
        "host_name", 
        "user_name", 
        "password", 
        immediate_connect= False, 
        client = FakeCQGClient()
        )
    
    async with MonitorDataCQG(conn) as MD:
        assert isinstance(MD, MonitorDataCQG)
        assert conn.state == ConnectionState.CONNECTED_DEFAULT

    # __aexit__ ran stop(), so connection should be fully torn down
    assert conn.state == ConnectionState.CLOSED

# --- Sad Paths aenter/aexit
async def  test_context_manager_failed_enter() -> None:
    ...
    
async def  test_context_manager_failed_exit() -> None:
    ...