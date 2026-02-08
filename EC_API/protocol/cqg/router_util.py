#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 06:21:10 2026

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg


def server_msg_type(msg: ServerMsg) -> str:
    
    
    pass

# Streaming classifiers (examples)
def is_realtime_tick(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"real_time_market_data"}

def is_order_update_stream(msg: ServerMsg) -> bool:
    # depending on CQG config you might get updates in trade_snapshot etc.
    return server_msg_type(msg) in {"order_statuses", "trade_snapshot"}


def is_trade_history(msg: ServerMsg) -> bool:
    return server_msg_type(msg) in {"information_report:historical_orders_report"}


