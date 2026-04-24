import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.parsers import connect_parsers
from EC_API.protocol.cqg.parser_util import parse_server_msg
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_symbol_resolution_report_server_msg,
    build_session_info_report_server_msg,
    build_option_maturity_list_report_server_msg,
    build_instrument_group_report_server_msg,
    build_historical_orders_report_server_msg,
    build_at_the_money_strike_report_server_msg,
    )
from EC_API.exceptions import MsgParserError


def test_parse_symbol_resolution_report_server_msg_valid() -> None:
    msg = build_symbol_resolution_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1
    
def test_parse_session_info_report_server_msg_valid() -> None:
    msg = build_session_info_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1

def test_option_maturity_list_report_server_msg() -> None:
    msg = build_option_maturity_list_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1


def test_parse_instrument_group_report_server_msg_valid()-> None:
    msg = build_instrument_group_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1

def test_parse_historical_orders_report_server_msg_valid()->None:
    msg = build_historical_orders_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1

def test_parse_at_the_money_strike_report_server_msg_valid()-> None:
    msg = build_at_the_money_strike_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1
