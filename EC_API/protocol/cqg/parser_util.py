#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 12:12:27 2025

@author: dexter
"""
# this parser function is needed to handle mixed sub message type in 
# information report, realtimedata and 


from typing import Callable, Any
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

def walk_fields(
        msg: ServerMsg, 
        selector: Callable[Any, Any],
        max_depth: int=2
    ):
    
    outs = []
    def walk(cur, depth):
        if depth > max_depth:
            return outs
        
        for fd, val in cur.ListField():
            # do something according to the field
            outs.extend(selector(fd,val))
            
            if fd.message_type is not None:
                if fd.is_repeated:
                    for ele in val:
                        walk(ele, depth+1)
                else:
                    walk(ele, depth+1)
    return walk(msg, 0)
    
type Parser_func = Callable[ServerMsg]
master_parsers: dict[str, Parser_func] = dict()

def register_parser(name):
    def decorator(func):
        master_parsers[name] = func
        return func
    return decorator
    

# =============================================================================
# def parse_information_report():...
# 
# 
# def parse_realtime_market_data():...
# 
# @register_parser('order_response')
# def parse_order_repsonse(msg):...
#     #"order_request_rejects": "rpc_reqid",
#     #"order_request_acks": "rpc_reqid",
#     #"trade_subscription_statuses": "sub",
#     #"trade_snapshot_completions": "sub",
#     #"order_statuses": "substream",
#     #"position_statuses": "substream",
#     #"account_summary_statuses": "substream",
#     #"go_flat_statuses": "rpc_reqid",
# =============================================================================
