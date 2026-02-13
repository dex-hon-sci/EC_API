#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 20:03:25 2026

@author: dexter
"""
from typing import Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from google.protobuf.descriptor import FieldDescriptor

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
@register_extractor('session')
def extract_session_router_keys(mt)->list[RouterKey]:
    return [("session", mt, "single", 0)]

@register_extractor('sub')
def extract_sub_router_keys()->list[RouterKey]: 
    return []

@register_extractor('substream')
def extract_substream_router_keys()->list[RouterKey]: 
    return []

@register_extractor('info')
def extract_info_keys(payload_list) -> list[RouterKey]:
    out = []
    for info in payload_list:
        info_id = getattr(info, "id", 0)
        present = [fd.name for fd, _ in info.ListFields()]
        typed = [n for n in present if n.endswith("_report") or n.endswith("_information_report")]
        if not typed:
            if info_id:
                out.append(("info", "information_reports", "info_id", int(info_id)))
            continue
        for sub in typed:
            if info_id:
                out.append(("info", f"information_reports:{sub}", "info_id", int(info_id)))
            else:
                out.append(("info", f"information_reports:{sub}", "none", 0))
    return out

@register_extractor('rpc')
def extract_rpc_router_keys(mt, payload_list)->list[RouterKey]:
    out = []
    for x in payload_list:
        rid = getattr(x, "request_id", 0)
        if rid:
            out.append(("rpc", mt, "request_id", int(rid)))
    return out

