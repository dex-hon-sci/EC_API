#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 00:10:29 2026

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_order_request_acks_server_msg,
    build_order_request_rejects_server_msg,
    build_trade_subscription_statuses_server_msg,
    build_trade_snapshot_completetions_server_msg,
    build_order_statuses_server_msg,
    build_position_statuses_server_msg,
    build_account_summary_statuses_server_msg,
    build_go_flat_statuses_server_msg
    )
from EC_API.ordering.cqg.parsers import (
    parse_order_request_rejects,
    parse_order_request_acks,
    parse_trade_subscription_statuses,
    parse_trade_snapshot_completetions,
    parse_order_statuses,
    parse_position_statuses,
    parse_account_summary_statuses,
    parse_go_flat_statuses
    )

def test_parse_order_request_rejects_server_msg_valid() -> None:
    msg = build_order_request_rejects_server_msg(ServerMsg(),request_id=2)
    res = parse_order_request_rejects(msg)
    
    assert isinstance(res, list)
    assert res[0]['request_id'] == 2
    assert res[0]['reject_code'] == 1001
     
    
def test_parse_order_request_acks_server_msg_valid() -> None:
    msg = build_order_request_acks_server_msg(ServerMsg(),request_id=3)
    res = parse_order_request_acks(msg)
    assert isinstance(res, list)
    assert res[0]['request_id'] == 3


def test_parse_trade_subscription_statuses_server_msg_valid() -> None:
    msg = build_trade_subscription_statuses_server_msg(ServerMsg())
    res = parse_trade_subscription_statuses(msg)
    assert isinstance(res, list)


def test_parse_trade_snapshot_completetions_server_msg_valid() -> None:
    msg = build_trade_snapshot_completetions_server_msg(ServerMsg())
    res = parse_trade_snapshot_completetions(msg)
    assert isinstance(res, list)


def test_parse_order_statuses_server_msg_valid() -> None:
    msg = build_order_statuses_server_msg(ServerMsg())
    parse_order_statuses(msg)

    
def test_parse_position_statuses_server_msg_valid() -> None:
    msg = build_position_statuses_server_msg(ServerMsg())
    parse_position_statuses(msg)

def test_parse_account_summary_statuses_server_msg_valid() -> None:
    msg = build_account_summary_statuses_server_msg(ServerMsg())

    parse_account_summary_statuses(msg)
    
def test_parse_go_flat_statuses_server_msg_valid() -> None:
    msg = build_go_flat_statuses_server_msg(ServerMsg())
    parse_go_flat_statuses(msg)
