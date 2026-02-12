#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 06:21:10 2026

@author: dexter
"""
from typing import Optional, Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

RouterKey = tuple[str, str, str, int|str]

type Extractor_func = Callable[ServerMsg]

_extractors: dict[str, Extractor_func] = {}


def register_extractors(msg_name: str):
    def decorator(func: Callable[..., None]):
        _extractors[msg_name] = func
        return func
    return decorator

def server_msg_type(msg: ServerMsg) -> str:
    return msg.WhichOneof("message")  # CQG oneof "message"


# Table-driven request_id extraction for RPC replies
def extract_router_key(msg: ServerMsg) -> Optional[Key]:
    mt = server_msg_type(msg)
    ...
    return 

# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"real_time_market_data"}

def is_order_update_stream(msg: ServerMsg) -> bool:
    # depending on CQG config you might get updates in trade_snapshot etc.
    return server_msg_type(msg) in {"order_statuses", "trade_snapshot"}

def is_trade_history(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"information_report:historical_orders_report"}

# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) == "real_time_market_data"

def is_order_update_stream(msg: ServerMsg) -> bool:
    # depending on CQG config you might get updates in trade_snapshot etc.
    return server_msg_type(msg) in {"order_statuses", "trade_snapshot"}

def is_trade_history(msg: ServerMsg) -> bool:
    return server_msg_type(msg)

# Helper to detect message types
def is_symbol_resolution(msg: ServerMsg) -> bool:
    return msg.WhichOneof("message") == "information_reports" \
        and len(msg.information_reports) > 0 \
        and msg.information_reports[0].HasField("symbol_resolution_report")

def is_realtime_tick(msg: ServerMsg) -> bool:
    return msg.WhichOneof("message") == "real_time_market_data" \
        and len(msg.real_time_market_data) > 0

def is_order_update(msg: ServerMsg) -> bool:
    return msg.WhichOneof("message") == "trade_snapshot" \
        or msg.WhichOneof("message") == "order_update"   # adjust to your proto