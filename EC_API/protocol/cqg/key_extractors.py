#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 20:03:25 2026

@author: dexter
"""
from typing import Callable
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

def register_extractor(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        _extractors[msg_name] = func
        return func
    return decorator

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

def extract_names_generic(
        msg: Message, 
        selection_func: Callable[Any, list],
        max_depth: int = 1,
    ) -> list[str]:
    
    out: list[str] = []

    def is_repeated_container(x: Any) -> bool:
        return isinstance(x, (RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer))

    def walk(cur: Any, depth: int) -> None:
        if depth > max_depth:
            return

        # Message: only iterate fields that are present
        if isinstance(cur, Message):
            for fd, val in cur.ListFields():
                #### Injection of selection function, condition for taking record
                record = selection_func(fd, val)
                out.extend(record)  
                ####
                # repeated field
                if fd.is_repeated:
                    if fd.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE:
                        # recurse into each element (NOT the container)
                        for elem in val:
                            walk(elem, depth + 1)
                    else:
                        # repeated scalar: nothing to recurse into
                        pass
                # singular field
                else:
                    if fd.cpp_type == FieldDescriptor.CPPTYPE_MESSAGE:
                        walk(val, depth + 1)
                    else:
                        # scalar: nothing to recurse into
                        pass
            return
        # If someone accidentally passes a repeated container, still handle it
        if is_repeated_container(cur):
            for elem in cur:
                walk(elem, depth + 1)
            return
        # scalar -> stop
        return
    walk(msg, 0)
    return out

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
    
    def selection_func(fd, val):
        if fd.message_type is None:
            return [fd.name, val]
        else:
            return [fd.name]
    out = extract_names_generic(msg,selection_func)
    res = []
    temp= [0,0,0,0]
    for i, ele in enumerate(out):
        if ele == 'information_reports':
            temp[0] = "info"
        if ele == 'id':
            temp[2] = ele
            temp[3] = out[i+1]
            
        if ele in MAP_RESPONSES_TYPES_STR.get("information_requests") and \
           ele !="information_reports":
            temp[1] = f"information_reports:{ele}"
    res.append(tuple(temp))
    return res


@register_extractor('sub')
def extract_sub_router_keys(
        msg: ServerMsg, 
        msg_type: str                      
    )->list[RouterKey]: 
    extract_names_generic()
    return []

@register_extractor('substream')
def extract_substream_router_keys()->list[RouterKey]: 
    return []


@register_extractor('rpc')
def extract_rpc_router_keys(mt, payload_list)->list[RouterKey]:
    out = []
    for x in payload_list:
        rid = getattr(x, "request_id", 0)
        if rid:
            out.append(("rpc", mt, "request_id", int(rid)))
    return out

