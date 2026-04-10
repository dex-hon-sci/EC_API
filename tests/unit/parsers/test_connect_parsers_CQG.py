import pytest
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
    build_pong_server_msg,
    build_symbol_resolution_report_server_msg
    )
from EC_API.exceptions import MsgParserError

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
    with pytest.raises(MsgParserError):
        parse_logon_result(None)
    
def test_parse_logged_off_null()-> None:
    with pytest.raises(MsgParserError):
        parse_logged_off(None)

def test_parse_restore_or_join_session_result_null()-> None:
    with pytest.raises(MsgParserError):
        parse_restore_or_join_session_result(None)

def test_parse_pong_null()-> None:
    with pytest.raises(MsgParserError):
        parse_pong(None)

# --- info report parsing
def test_parse_symbol_resolution_report_valid() -> None:
    msg = build_symbol_resolution_report_server_msg(ServerMsg())
    res = parse_symbol_resolution_report(msg)
    assert isinstance(res, list)