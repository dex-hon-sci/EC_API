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
    conn._timeout = 0.5
    return conn, ft


async def _inject_after_send(
        fake_transport: FakeTransport,
        response: ServerMsg
    ) -> None:
    """Wait for an outbound message then inject a server response."""
    await asyncio.wait_for(fake_transport.out_q.get(), timeout = 0.5)
    await fake_transport.in_q.put(response)
    
# --- 
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
    print(result)

    assert result is not None
    assert conn.state == ConnectionState.LOGGED_ON
    await conn.stop()
    
# =============================================================================
# @pytest.mark.asyncio
# def test_logoff_call():...
# 
# @pytest.mark.asyncio
# def test_restore_call():...
# 
# @pytest.mark.asyncio
# def test_ping_call():...
# 
# @pytest.mark.asyncio
# def test_resolve_symbol_call():...
# 
# =============================================================================
