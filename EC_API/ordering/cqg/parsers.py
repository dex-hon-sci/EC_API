#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 03:05:48 2026

@author: dexter
"""
from typing import Any
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.parser_util import register_parser
from EC_API.exceptions import MsgParserError

@register_parser('order_request_rejects')
def parse_order_request_rejects(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    try:
        res = []
        for ele in msg.order_request_rejects: 
            res.append(
                {'resquest_id':ele.request_id,
                 'reject_code':ele.reject_code}
                )
        return res
    except Exception:
        raise MsgParserError("Failed to parse order_request_rejects.")
        
@register_parser('order_request_acks')
def parse_order_request_acks(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    try:
        res = []
        for ele in msg.order_request_acks:
            res.append(
                {'resquest_id': ele.request_id,
                 'when': ele.when
                 }
                )
        return res
    except Exception:
        raise MsgParserError("Failed to parse order_request_acks.")

@register_parser('trade_subscription_statuses')
def parse_trade_subscription_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:

    try:
        res = []
        for ele in msg.trade_subscription_statuses:
            res.append(
                {'sub_id': ele.id,
                 'status_code': ele.status_code
                 }
                )
        return res
    except Exception:
        raise MsgParserError("Failed to parse trade_subscription_statuses.")
        
@register_parser('trade_snapshot_completetions')
def parse_trade_snapshot_completetions(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:

    try:
        res = []
        for ele in msg.trade_snapshot_completions:
            res.append({
                "sub_id": ele.subscription_id,
                "sub_scope": ele.subscription_scopes
                })
    except Exception:
        raise MsgParserError("Failed to parse trade_snapshot_completions.")

@register_parser('order_statuses')
def parse_order_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    try:
        res = []
    except Exception:
        raise MsgParserError("Failed to parse order_statuses.")

@register_parser('position_statuses')
def parse_position_statuses(msg:ServerMsg):
    ...
@register_parser('account_summary_statuses')
def parse_account_summary_statuses(msg:ServerMsg):
    ...

@register_parser('go_flat_statuses')    
def parse_go_flat_statuses(msg:ServerMsg):
    ...
