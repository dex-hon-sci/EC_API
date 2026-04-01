#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:08:53 2026

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API._typing import (
    LogonResultType,
    )
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
    return

def test_parse_restore_or_join_session_result_valid() -> None:
    ...

def test_parse_pong() -> None:
    ...
    
def test_parse_symbol_resolution_report() -> None:
    ...