#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 10:11:09 2025

@author: dexter
"""

# EC_API/protocol/cqg/routing.py
from __future__ import annotations
from typing import Optional, Tuple
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

Key = Tuple[str, int]

def server_msg_type(msg: ServerMsg) -> str:
    return msg.WhichOneof("message")  # CQG oneof "message"

# Table-driven request_id extraction for RPC replies
def extract_router_key(msg: ServerMsg) -> Optional[Key]:
    mt = server_msg_type(msg)

    # Only include RPC-ish reply types here
    if mt == "information_reports":
        # Often list; take first item for request_id
        if len(msg.information_reports) == 0:
            return None
        rid = msg.information_reports[0].request_id
        return (mt, rid)

    if mt == "user_session_statuses":
        return (mt, msg.user_session_statuses.request_id)

    if mt == "market_data_subscription_statuses":
        return (mt, msg.market_data_subscription_statuses.request_id)

    if mt == "trade_subscription_statuses":
        return (mt, msg.trade_subscription_statuses.request_id)

    if mt == "order_statuses":
        return (mt, msg.order_statuses.request_id)

    # add more as needed
    return None


# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) == "real_time_market_data"

def is_order_update_stream(msg: ServerMsg) -> bool:
    # depending on CQG config you might get updates in trade_snapshot etc.
    return server_msg_type(msg) in {"order_statuses", "trade_snapshot"}

