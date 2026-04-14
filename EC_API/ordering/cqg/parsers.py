#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 03:05:48 2026

@author: dexter
"""
from typing import Any
from google.protobuf.json_format import MessageToDict
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
                {'request_id':ele.request_id,
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
                {'request_id': ele.request_id,
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
        
@register_parser('trade_snapshot_completions')
def parse_trade_snapshot_completions(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:

    try:
        res = []
        for ele in msg.trade_snapshot_completions:
            print('ele', ele)
            res.append({
                "sub_id": ele.subscription_id,
                "sub_scopes": list(ele.subscription_scopes)
                })
        return res
    except Exception:
        raise MsgParserError("Failed to parse trade_snapshot_completions.")

@register_parser('order_statuses')
def parse_order_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    try:
        res = []
        for i, ele in enumerate(msg.order_statuses):
            D = {
                "sub_ids": list(ele.subscription_ids),
                "order_id": ele.order_id,
                "chain_order_id": ele.chain_order_id,
                "status_utc_timestamp": ele.status_utc_timestamp,
                "submission_utc_timestamp": ele.submission_utc_timestamp,
                "fill_cnt": ele.fill_cnt,
                "scaled_avg_fill_price": ele.scaled_avg_fill_price,
                "avg_fill_price_correct": ele.avg_fill_price_correct,
                "account_id": ele.account_id
                }
            if ele.HasField('order'):
                D['order'] = {
                    'account_id': ele.order.account_id,
                    'cl_order_id': ele.order.cl_order_id,
                    'contract_id': ele.order.contract_id,
                    'order_type': ele.order.order_type,
                    'duration': ele.order.duration,
                    'side': ele.order.side,
                    'qty': {'significand': ele.order.qty.significand,
                            'exponent':ele.order.qty.exponent}
                    }
            res.append(D)
        return res
    
    except Exception as e:
        raise MsgParserError(f"Failed to parse order_statuses: {e}") from e

@register_parser('position_statuses')
def parse_position_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:

    try:
        res = []
        for i, ele in enumerate(msg.position_statuses):
            ...
        return res
    
    except Exception as e:
        raise MsgParserError(f"Failed to parse position_statuses: {e}") from e

    
@register_parser('account_summary_statuses')
def parse_account_summary_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    
    try:
        res = []
        for ele in msg.account_summary_statuses:
            res.append({
                'subscription_ids': ele.subscription_ids,
                'account_id': ele.account_id,
                'currency': ele.currency,
                'purchasing_power': ele.purchasing_power
                })
        return res
    except Exception as e:
        raise MsgParserError(f"Failed to parse account_summary_statuses: {e}") from e
 

@register_parser('go_flat_statuses')    
def parse_go_flat_statuses(
        msg:ServerMsg
    ) -> list[dict[str, Any]]:
    try:
        res = []
        for ele in msg.go_flat_statuses:
            res.append({
                'request_id': ele.request_id,
                'account_id': ele.account_id,
                'status_code': ele.status_code
                })
        return res
    except Exception as e:
        raise MsgParserError(f"Failed to parse go_flat_statuses: {e}") from e
