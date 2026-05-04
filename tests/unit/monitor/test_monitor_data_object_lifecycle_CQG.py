#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:20:21 2026

@author: dexter
"""
import asyncio
import pytest
import logging
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.exceptions import ConnectEnterError
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_symbol_resolution_report_server_msg
    )
from tests.unit.fixtures.proxy_clients import FakeTransport, FakeCQGClient
from tests.unit.fixtures.dummy_server_CQG import FakeDataServerCQG


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
@pytest.mark.asyncio
async def test_aenter_raises_on_conn_failure(mocker):
    mock_conn = mocker.MagicMock()
    mock_conn.__aexit__ = mocker.AsyncMock()

    monitor = MonitorDataCQG.__new__(MonitorDataCQG)
    monitor._conn = mock_conn
    monitor._cleanup = mocker.AsyncMock(side_effect=RuntimeError("unexpected"))

    with pytest.raises(RuntimeError):
        await monitor.__aexit__(None, None, None)

    mock_conn.__aexit__.assert_called_once()  # fails with current code

@pytest.mark.asyncio
async def test_aexit_conn_called_even_if_cleanup_raises(mocker):
    mock_conn = mocker.MagicMock()
    mock_conn.__aexit__ = mocker.AsyncMock()

    monitor = MonitorDataCQG.__new__(MonitorDataCQG)
    monitor._conn = mock_conn
    monitor._cleanup = mocker.AsyncMock(side_effect=RuntimeError("unexpected"))

    with pytest.raises(RuntimeError):
        await monitor.__aexit__(None, None, None)

    mock_conn.__aexit__.assert_called_once()  # fails with current code


@pytest.mark.asyncio
async def test_aexit_normal(mocker):
    mock_conn = mocker.MagicMock()
    mock_conn.__aexit__ = mocker.AsyncMock()

    monitor = MonitorDataCQG.__new__(MonitorDataCQG)
    monitor._conn = mock_conn
    monitor._cleanup = mocker.AsyncMock()

    result = await monitor.__aexit__(None, None, None)

    monitor._cleanup.assert_awaited_once()
    mock_conn.__aexit__.assert_awaited_once_with(None, None, None)
    assert result is False

# --- Cleanup Success ---
@pytest.mark.asyncio
async def test_context_manager_automatic_cleanup_upon_exit_success() -> None:
    ft = FakeTransport()
    conn = ConnectCQG(
        "host_name", 
        "user_name", 
        "password", 
        immediate_connect= False, 
        client = FakeCQGClient(),
        transport = ft
        )
    
    sr = SymbolRegistry()
    MD = MonitorDataCQG(conn)
    MD._symbol_registry = sr
    
    # First register a symbol info
    MD._symbol_registry.register("asset_A", {'contract_id':1})
    MD._symbol_registry.register("asset_B", {'contract_id':2})
    MD._symbol_registry.register("asset_C", {'contract_id':3})
    
    async def run_MD():
        async with MD:
            assert isinstance(MD, MonitorDataCQG)

    async def grab_and_respond(n: int) -> None:
        loop = asyncio.get_running_loop()
        for _ in range(n):
            client_msg = await loop.run_in_executor(None, ft.out_q.get)
            req = client_msg.information_requests[0]
            assert req.subscribe == False
            symbol = req.symbol_resolution_request.symbol   # use whatever came in
            response = build_symbol_resolution_report_server_msg(
                ServerMsg(), report_id=req.id, contract_symbol=symbol
            )
            await ft.in_q.put(response)
    
    await asyncio.gather(run_MD(), grab_and_respond(3))
    
    assert not MD._symbol_registry.active_symbols
    assert not MD._symbol_registry.metatdata
    
# --- Cleanup Fail ---
@pytest.mark.asyncio
async def test_context_manager_automatic_cleanup_upon_exit_fail_timeout(caplog) -> None:
    ft = FakeTransport()
    conn = ConnectCQG(
        "host_name", 
        "user_name", 
        "password", 
        immediate_connect= False, 
        client = FakeCQGClient(),
        transport = ft
        )
    conn._timeout = 0.001
    sr = SymbolRegistry()
    MD = MonitorDataCQG(conn)
    MD._symbol_registry = sr
    
    # First register a symbol info
    MD._symbol_registry.register("asset_A", {'contract_id':1})
    MD._symbol_registry.register("asset_B", {'contract_id':2})
    MD._symbol_registry.register("asset_C", {'contract_id':3})
    
    async def run_MD():
        async with MD:
            assert isinstance(MD, MonitorDataCQG)

    with caplog.at_level(logging.ERROR, logger="EC_API.connect.cqg.base"):
        await run_MD() # no response message -> timeout
        await asyncio.sleep(0)

    
