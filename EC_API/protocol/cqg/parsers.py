#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 12:12:27 2025

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

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