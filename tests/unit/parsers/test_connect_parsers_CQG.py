#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:08:53 2026

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.parsers import (
    parse_logon_result,
    parse_logged_off,
    parse_restore_or_join_session_result,
    parse_pong,
    parse_symbol_resolution_report
    )
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_logon_result_server_msg,
    build_logged_off_server_msg,
    build_restore_or_join_session_result_server_msg,
    build_pong_server_msg
    )
def test_parse_logon_result_valid()->None:
    s = ServerMsg()
    msg = build_logon_result_server_msg(s)
    res = parse_logon_result(msg)
    assert isinstance(res, dict) 
    assert len(res) == 3
    for k, v in res.items():
        assert k in ("result_code", "base_time", "server_time")

def test_parse_logged_off_valid()->None:
    s = ServerMsg()
    msg = build_logged_off_server_msg(s)
    res = parse_logged_off(msg)
    assert isinstance(res, dict) 
    assert len(res) == 1
    for k, v in res.items():
        assert k in ("logoff_reason")

def test_parse_restore_or_join_session_result_valid() -> None:
    s = ServerMsg()
    msg = build_restore_or_join_session_result_server_msg(s)
    res = parse_restore_or_join_session_result(msg)
    assert isinstance(res, dict) 
    assert len(res) == 3
    for k, v in res.items():
        assert k in ("result_code", "base_time", "server_time")

def test_parse_pong_valid() -> None:
    s = ServerMsg()
    msg = build_pong_server_msg(s, 'token')
    res = parse_pong(msg)
    assert isinstance(res, tuple) 
    assert len(res) == 4
    assert res[0] == "pong"
    assert res[1] == "token"

def test_parse_logon_result_null()-> None:
    res = parse_logon_result(None)
    assert res is None
    
def test_parse_logged_off_null()-> None:
    res = parse_logged_off(None)
    assert res is None

def test_parse_restore_or_join_session_result_null()-> None:
    res = parse_restore_or_join_session_result(None)
    assert res is None

def test_parse_pong_null()-> None:
    res = parse_pong(None)
    assert res is None


# --- info report parsing
    
def test_parse_symbol_resolution_report() -> None:
    ...