import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, InformationReport
from EC_API.ext.common.shared_1_pb2 import OrderStatus, TransactionStatus
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
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    # --- ContractMetaData
    assert res[0]['contract_metadata']['contract_id'] == 3
    assert res[0]['contract_metadata']['contract_symbol'] == 'CLE'
    assert res[0]['contract_metadata']['correct_price_scale'] == 100.0
    assert res[0]['contract_metadata']['display_price_scale'] == 200
    assert res[0]['contract_metadata']['description'] == 'Desc'
    assert res[0]['contract_metadata']['title'] == 'Test CLE title'
    assert res[0]['contract_metadata']['tick_size'] == 10.0
    assert res[0]['contract_metadata']['currency'] == 'USD'
    assert res[0]['contract_metadata']['tick_value'] == 23.0
    assert res[0]['contract_metadata']['cfi_code'] == 'cfi_code'
    assert res[0]['contract_metadata']['instrument_group_name'] == 'Crude Oil'
    assert res[0]['contract_metadata']['session_info_id'] == 214
    assert res[0]['contract_metadata']['short_instrument_group_name'] == ''
    assert res[0]['contract_metadata']['instrument_group_description'] == ''
    assert res[0]['contract_metadata']['country_code'] == 'AUS'

def test_parse_session_info_report_server_msg_valid() -> None:
    msg = build_session_info_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)

    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    assert res[0]['session_info_id'] == 330
    assert res[0]['session_segments'] == [{'session_segment_id': '1111'}]

def test_option_maturity_list_report_server_msg() -> None:
    msg = build_option_maturity_list_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)

    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    assert res[0]['option_maturities'] == [
        {'id': 'id_1', 'name': 'CLXXXX', 'description': 'description'}
        ]
    
def test_parse_instrument_group_report_server_msg_valid()-> None:
    msg = build_instrument_group_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)

    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    assert res[0]['instruments'] == [
        {'id': 'id_1', 'name': 'Instrument_1', 
         'description': 'description'}
        ]
    
def test_parse_historical_orders_report_server_msg_valid()->None:
    msg = build_historical_orders_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)
    
    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    assert isinstance(res[0]['order_statuses'], list)  
    assert res[0]['order_statuses'][0]['status'] == OrderStatus.Status.FILLED
    assert res[0]['order_statuses'][0]['order_id'] == '1' 
    assert res[0]['order_statuses'][0]['chain_order_id'] == 'A'
    assert res[0]['order_statuses'][0]['fill_cnt'] == 1
    
def test_parse_at_the_money_strike_report_server_msg_valid()-> None:
    msg = build_at_the_money_strike_report_server_msg(ServerMsg())
    res = parse_server_msg(msg, connect_parsers)

    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['id'] == 1
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    assert res[0]['strike'] == 100
    
# ── Group 1: MsgParserError is raised ────────────────────────────────────────

def test_parse_server_msg_empty_msg_raises_error() -> None:
    # parse_server_msg cannot resolve msg type from a blank ServerMsg
    with pytest.raises(MsgParserError, match="Cannot resolve server message type"):
        parse_server_msg(ServerMsg(), connect_parsers)


def test_parse_server_msg_empty_parsers_dict_raises_error() -> None:
    # valid information_reports msg but empty parsers dict → no parser found
    msg = build_symbol_resolution_report_server_msg(ServerMsg())
    with pytest.raises(MsgParserError, match="does not exist"):
        parse_server_msg(msg, {})


# ── Group 2: Failure/error status codes — parsers don't raise, return status ─

def test_parse_symbol_resolution_report_status_code_failure() -> None:
    msg = build_symbol_resolution_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE


def test_parse_symbol_resolution_report_status_code_not_found() -> None:
    msg = build_symbol_resolution_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_NOT_FOUND
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_NOT_FOUND


def test_parse_session_info_report_status_code_failure() -> None:
    msg = build_session_info_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE


def test_parse_historical_orders_report_status_code_failure() -> None:
    msg = build_historical_orders_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE


def test_parse_option_maturity_list_report_status_code_failure() -> None:
    msg = build_option_maturity_list_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE


def test_parse_instrument_group_report_status_code_failure() -> None:
    msg = build_instrument_group_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE


def test_parse_at_the_money_strike_report_status_code_failure() -> None:
    msg = build_at_the_money_strike_report_server_msg(
        ServerMsg(), res=InformationReport.StatusCode.STATUS_CODE_FAILURE
    )
    res = parse_server_msg(msg, connect_parsers)
    assert res[0]['status_code'] == InformationReport.StatusCode.STATUS_CODE_FAILURE