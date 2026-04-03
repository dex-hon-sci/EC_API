#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:18:05 2026

@author: dexter
"""
import asyncio
import pytest
import time
from unittest.mock import patch
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.transport.routers import MessageRouter
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, ClientMsg
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LgRes
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as RstJoinSessRes
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LgOff
from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as InfoRp

from tests.unit.fixtures.proxy_clients import FakeTransport
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_logon_result_server_msg,
    build_logged_off_server_msg,
    build_restore_or_join_session_result_server_msg,
    build_pong_server_msg,
)

def make_conn() -> tuple[ConnectCQG, FakeTransport]:
    conn = ConnectCQG(
        host_name="", user_name="test_user", password="test_pass",
        immediate_connect=False, client=object()
    )
    ft = FakeTransport()
    conn._transport = ft
    conn._timeout = 0.1
    return conn, ft


async def _inject_after_send(
        fake_transport: FakeTransport,
        response: ServerMsg
    ) -> None:
    """Wait for an outbound message then inject a server response."""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, fake_transport.out_q.get)
    await fake_transport.in_q.put(response)
    
# --- logon tests
@pytest.mark.asyncio
async def test_logon_call_success() -> None:
    conn, ft = make_conn()
    conn.start()

    response = build_logon_result_server_msg(
        ServerMsg(), 
        res_code = LgRes.ResultCode.RESULT_CODE_SUCCESS
        )  # SUCCESS

    result, _ = await asyncio.gather(
        conn.logon(),
        _inject_after_send(ft, response)
    )

    assert result is not None
    assert result['result_code'] == LgRes.ResultCode.RESULT_CODE_SUCCESS
    assert conn.state == ConnectionState.CONNECTED_LOGON
    await conn.stop()
    
# --- Logoff tests
@pytest.mark.asyncio
async def test_logoff_call_success() -> None:
    conn, ft = make_conn()
    conn.start()

    response = build_logged_off_server_msg(
        ServerMsg(), 
        res = LgOff.LogoffReason.LOGOFF_REASON_BY_REQUEST
        )  

    result, _ = await asyncio.gather(
        conn.logoff(),
        _inject_after_send(ft, response)
    )

    assert result is not None
    assert result['logoff_reason'] == LgOff.LogoffReason.LOGOFF_REASON_BY_REQUEST
    assert conn.state == ConnectionState.CONNECTED_LOGOFF
    await conn.stop()

# --- restore tests
@pytest.mark.asyncio
async def test_restore_request_success() -> None:
    conn, ft = make_conn()
    conn.start()
    
    response = build_restore_or_join_session_result_server_msg(
        ServerMsg(), RstJoinSessRes.ResultCode.RESULT_CODE_SUCCESS)
    #await ft.in_q.put(response)

    result, _ = await asyncio.gather(
        conn.restore_request("session_token","client_app_id",0,0),
        _inject_after_send(ft, response)
    )
    #result = await conn.restore_request("session_token","client_app_id",0,0)
    assert result is not None
    assert result['result_code'] == RstJoinSessRes.ResultCode.RESULT_CODE_SUCCESS
    assert conn.state == ConnectionState.CONNECTED_LOGON
    await conn.stop()

# --- ping tests
@pytest.mark.asyncio
async def test_ping_success() -> None:
    conn, ft = make_conn()
    conn.start()
    
    response = build_pong_server_msg(ServerMsg(), token="token_1")
    await ft.in_q.put(response)
    
    result = await conn.ping("token_1")
    assert result is not None
    assert result[1] == "token_1"
    await conn.stop()

# ============================================================================= 
# @pytest.mark.asyncio
# def test_resolve_symbol_call():...
# 
# =============================================================================
# test_logon_failure_result_code
# test_logon_timeout
# test_logon_sends_correct_credentials
# test_logoff_timeout
# test_restore_request_timeout
# test_restore_request_uses_stored_token
# test_ping_token_matches_pong
# test_ping_timeout
# test_ping_wrong_token_does_not_resolve
# 
# =============================================================================
# =============================================================================
