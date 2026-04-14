#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:10:29 2026

@author: dexter
"""
import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus as GFltStatus

from EC_API.ordering.enums import (Side)
from EC_API.ordering.cqg.builders import (
    build_new_order_request_msg
    )
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_order_request_acks_server_msg,
    build_order_request_rejects_server_msg,
    build_trade_subscription_statuses_server_msg,
    build_trade_snapshot_completions_server_msg,
    build_order_statuses_server_msg,
    build_position_statuses_server_msg,
    build_account_summary_statuses_server_msg,
    build_go_flat_statuses_server_msg
    )
from EC_API.ordering.cqg.parsers import (
    parse_order_request_rejects,
    parse_order_request_acks,
    parse_trade_subscription_statuses,
    parse_trade_snapshot_completions,
    parse_order_statuses,
    parse_position_statuses,
    parse_account_summary_statuses,
    parse_go_flat_statuses
    )
from EC_API.exceptions import (MsgParserError)

def test_parse_order_request_rejects_server_msg_valid() -> None:
    msg = build_order_request_rejects_server_msg(ServerMsg(), request_id=2)
    res = parse_order_request_rejects(msg)
    assert isinstance(res, list)
    assert res[0]['request_id'] == 2
    assert res[0]['reject_code'] == 1001
     
    
def test_parse_order_request_acks_server_msg_valid() -> None:
    msg = build_order_request_acks_server_msg(ServerMsg(), request_id=3)
    res = parse_order_request_acks(msg)
    assert isinstance(res, list)
    assert res[0]['request_id'] == 3


def test_parse_trade_subscription_statuses_server_msg_valid() -> None:
    msg = build_trade_subscription_statuses_server_msg(ServerMsg())
    res = parse_trade_subscription_statuses(msg)
    assert isinstance(res, list)


def test_parse_trade_snapshot_completions_server_msg_valid() -> None:
    msg = build_trade_snapshot_completions_server_msg(ServerMsg(),sub_id = 3)
    res = parse_trade_snapshot_completions(msg)
    assert isinstance(res, list)
    assert res[0]['sub_id'] == 3
    assert res[0]['sub_scopes'] == [1,2,3,4]


def test_parse_order_statuses_server_msg_valid() -> None:
    client_msg = build_new_order_request_msg(
        123466,
        10, # request_id
        10, # contract_id
        "cl_order_1", 
        Side.SELL, 
        111, 
        2)
    msg = build_order_statuses_server_msg(
        ServerMsg(),
        order = client_msg.order_requests[0].new_order.order)
    res = parse_order_statuses(msg)

    assert isinstance(res, list)
    assert len(res) == 1
    assert res[0]['sub_ids'] == [1]
    assert res[0]['order_id'] == 'order_id_1'
    assert res[0]['chain_order_id'] == 'chain_order_id_1'
    assert res[0]['fill_cnt'] == 0
    assert res[0]['scaled_avg_fill_price'] == -200
    assert res[0]['avg_fill_price_correct'] == 10.0
    assert res[0]['account_id'] == 123466
    
    assert res[0]['order']['account_id'] == 123466
    assert res[0]['order']['contract_id'] == 10
    assert res[0]['order']['cl_order_id'] == 'cl_order_1'
    assert res[0]['order']['side'] == 2
    assert res[0]['order']['qty']['significand'] == 111
    assert res[0]['order']['qty']['exponent'] == 2
    
def test_parse_position_statuses_server_msg_valid() -> None:
    msg = build_position_statuses_server_msg(ServerMsg())
    parse_position_statuses(msg)

def test_parse_account_summary_statuses_server_msg_valid() -> None:
    msg = build_account_summary_statuses_server_msg(ServerMsg())
    res = parse_account_summary_statuses(msg)
    assert isinstance(res, list)
    assert res[0]['subscription_ids'] == [1,2,3]
    assert res[0]['account_id'] == 1210221
    assert res[0]['currency'] == "USD"
    assert res[0]['purchasing_power'] == 1_000_000

def test_parse_go_flat_statuses_server_msg_valid() -> None:
    msg = build_go_flat_statuses_server_msg(ServerMsg())
    res = parse_go_flat_statuses(msg)
    assert isinstance(res, list)
    assert res[0]['request_id'] == 1
    assert res[0]['account_id'] == 1210221
    assert res[0]['status_code'] == GFltStatus.StatusCode.STATUS_CODE_COMPLETED


# --- Sad Path
def test_parse_order_request_rejects_null() -> None:
      with pytest.raises(MsgParserError):
          parse_order_request_rejects(None)

def test_parse_order_request_acks_null() -> None:
    with pytest.raises(MsgParserError):
        parse_order_request_acks(None)

def test_parse_trade_subscription_statuses_null() -> None:
    with pytest.raises(MsgParserError):
        parse_trade_subscription_statuses(None)

def test_parse_trade_snapshot_completions_null() -> None:
    with pytest.raises(MsgParserError):
        parse_trade_snapshot_completions(None)

def test_parse_order_statuses_null() -> None:
    with pytest.raises(MsgParserError):
        parse_order_statuses(None)

def test_parse_position_statuses_null() -> None:
    with pytest.raises(MsgParserError):
        parse_position_statuses(None)

def test_parse_account_summary_statuses_null() -> None:
    with pytest.raises(MsgParserError):
        parse_account_summary_statuses(None)

def test_parse_go_flat_statuses_null() -> None:
    with pytest.raises(MsgParserError):
        parse_go_flat_statuses(None)