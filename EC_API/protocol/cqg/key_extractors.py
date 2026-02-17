#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 20:03:25 2026

@author: dexter
"""
from typing import Callable, Any, Iterable
from dataclasses import dataclass
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer, 
    RepeatedScalarFieldContainer
    )
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.mapping import MAP_RESPONSES_TYPES_STR
#("session", "logon_result", "singleton", 0)
#("report", "information_reports:historical_orders_report", "request_id", 1234)
#("md_sub", "market_data_subscription_statuses", "request_id", 20001)
#("trade_sub", "trade_subscription_statuses", "subscription_id", 55555)
#("order_ack", "order_request_rejects", "request_id", 30001)
RouterKey = tuple[str, str, str, int|str]
type Extractor_func = Callable[ServerMsg]
_extractors: dict[str, Extractor_func] = {}

@dataclass(frozen=True)
class KeyHit:
    name: str
    value: Any | None
    is_repeated: bool
    is_message: bool
    
def register_extractor(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        _extractors[msg_name] = func
        return func
    return decorator

SERVER_MSG_FAMILY = {
    # (1) connection/session
    "logon_result": "session",
    "restore_or_join_session_result": "session",
    "concurrent_connection_join_results": "session",
    "logged_off": "session",
    "pong": "session",
    # (2) info report container
    "information_reports": "info",
    # (3) order/account RPC & streams
    "order_request_rejects": "rpc_reqid",
    "order_request_acks": "rpc_reqid",
    "trade_subscription_statuses": "sub",
    "trade_snapshot_completions": "sub",
    "order_statuses": "substream",
    "position_statuses": "substream",
    "account_summary_statuses": "substream",
    "go_flat_statuses": "rpc_reqid",
    # (4) realtime
    "market_data_subscription_statuses":  "md",
    "real_time_market_data": "mdstream",
    # (5) historical
    "time_and_sales_reports": "rpc_reqid",
    "time_bar_reports": "rpc_reqid",
    "volume_profile_reports": "rpc_reqid",
    "non_timed_bar_reports": "rpc_reqid",
}
#########33

from typing import Any
from google.protobuf.message import Message

def walk_fields(
        msg: Message, 
        selector: Callable[[Any, Any], Iterable[KeyHit]],
        max_depth: int = 1,
    ) -> list[KeyHit]:
    
    outs: list[KeyHit] = []

    def walk(cur: Any, depth: int) -> None:
        if depth > max_depth:
            return

        # Message: only iterate fields that are present
        if not isinstance(cur, Message):
            return 
        
        for fd, val in cur.ListFields():   
            #### Inject selection function, condition for taking record
            outs.extend(selector(fd, val))

            # Recursvie Descend
            if fd.message_type is not None:
                if fd.is_repeated:# repeated field
                    for elem in val:
                        walk(elem, depth + 1)
                else:# singular field
                    walk(val, depth + 1)
                    
    walk(msg, 0)
    return outs

@register_extractor('session')
def extract_session_router_keys(
        msg: ServerMsg, 
        msg_type: str
    )->list[RouterKey]:
    return [("session", msg_type, "single", 0)]


@register_extractor('info')
def extract_info_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]:
    
    TARGET = {                             
        "symbol_resolution_report",
        "session_information_report",
        "historical_orders_report",
        "option_maturity_list_report",
        "instrument_group_report",
        "at_the_money_strike_report"
    }
    
    MAP_RESPONSES_TYPES_STR.get("information_requests")
    
    def selector(fd, val) -> Iterable[KeyHit]:
        if fd.message_type is not None and (fd.name in TARGET or fd.name == "information_reports"):
            yield KeyHit(fd.name, None, fd.is_repeated, True)
        
        else:
            if fd.name == 'id' and not fd.is_repeated:             
                yield KeyHit(fd.name, val, fd.is_repeated, False)

    outs = walk_fields(msg, selector, max_depth=1)
    
    report_type, request_id = None, None  
    sub_report_type = ""
    for hit in outs:
        if report_type is None and hit.name == "information_reports":
            report_type = hit.name
        if sub_report_type == "" and hit.name in TARGET:
            sub_report_type = ":"+hit.name
        if request_id is None and hit.name == 'id':
            request_id = hit.value

    if report_type is None or request_id is None:
        return []

    return [("info", report_type+sub_report_type, 
             "id", request_id)]

@register_extractor("rpc_reqid")
def extract_rpc_reqid_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]:
    
    TARGET = {
        "order_request_rejects", 
        "order_request_acks",
        "go_flat_statuses",
        "time_and_sales_reports",
        "time_bar_reports",
        "volume_profile_reports",
        "non_timed_bar_reports"
    }
    
    def selector(fd, val) -> Iterable[KeyHit]:
        if fd.message_type is not None and fd.name in TARGET:
            yield KeyHit(fd.name, None, fd.is_repeated, True)
        else:
            if fd.name == 'request_id' and not fd.is_repeated:        
                yield KeyHit(fd.name, val, fd.is_repeated, False)
    
    outs = walk_fields(msg, selector, max_depth=2)
    
    report_type, request_id = None, None  
    for hit in outs:
        if report_type is None and hit.name in TARGET:
            report_type = hit.name
        if request_id is None and hit.name == 'request_id':
            request_id = hit.value

    if report_type is None or request_id is None:
        return []

    return [("rpc_reqid", report_type, "request_id", request_id)]

@register_extractor('sub')
def extract_sub_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ) -> list[RouterKey]: 
    walk_fields()
    return []

@register_extractor('substream')
def extract_substream_router_keys()->list[RouterKey]: 
    return []


@register_extractor('md')
def extract_market_data_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    ):
    
    def selector(fd, val)-> Iterable[KeyHit]:...

@register_extractor('md_stream')
def extract_market_data_stream_router_keys():...

# =============================================================================
# SERVER_MSG_FAMILY = {
#   # (1) connection/session
#   "LogonResult": "session",
#   "RestoreOrJoinSessionResult": "session",
#   "ConcurrentConnectionJoin": "session",
#   "LoggedOff": "session",
#   "Pong": "session",
#   # (2) info report container
#   "InformationReport": "info",
#   # (3) order/account RPC & streams
#   "OrderRequestReject": "rpc_reqid",
#   "OrderRequestAck": "rpc_reqid",
#   "GoFlatStatus": "rpc_reqid",
#   "TradeSubscriptionStatus": "sub",           # keyed by .id in your builder
#   "TradeSnapshotCompletion": "sub",            # keyed by subscription_id
#   "OrderStatus": "substream",                  # keyed by subscription_ids
#   "PositionStatus": "substream",
#   "AccountSummaryStatus": "substream",
#   # (4) realtime
#   "MarketDataSubscriptionStatus": "md",      # keyed by contract_id in your builder
#   "RealTimeMarketData": "mdstream",            # keyed by contract_id
#   # (5) historical
#   "TimeAndSalesReport": "rpc_reqid",
#   "TimeBarReport": "rpc_reqid",
#   "VolumeProfileReport": "rpc_reqid",
#   "NonTimedBarReport": "rpc_reqid",
# }
# =============================================================================
