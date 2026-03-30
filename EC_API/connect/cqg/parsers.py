#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 02:39:15 2026

@author: dexter
"""
from typing import Any, Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

def parse_logon_result(server_msg: ServerMsg | None) -> dict[str, Any]:
    if not server_msg:
        return 
    
    return {
        "result_code": server_msg.logon_result.result_code,
        "base_time": server_msg.logon_result.base_time,
        "server_time": server_msg.logon_result.server_time
        }

def parse_restore_or_join_session_result(server_msg: ServerMsg | None) -> dict[str, Any]:
    if not server_msg:
        return 

    return {
        "result_code": server_msg.restore_or_join_session_result.result_code,
        "base_time": server_msg.restore_or_join_session_result.base_time,
        "server_time": server_msg.restore_or_join_session_result.server_time
        }
    
def parse_logged_off(server_msg: ServerMsg | None) -> dict[str, Any]: 
    if not server_msg:
        return 

    return {
        "logoff_reason": server_msg.logged_off.logoff_reason,
        }

def parse_pong(server_msg: ServerMsg | None) -> tuple[str, int, int]:
    if not server_msg:
        return 

    return ("pong", server_msg.pong.ping_utc_time, server_msg.pong.pong_utc_time)

# Meta data parsers
type Parser_func = Callable[ServerMsg]
metadata_parsers: dict[str, Parser_func] = {}

def register_info_report_parsers(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        metadata_parsers[msg_name] = func
        return func
    return decorator

@register_info_report_parsers('symbol_resoluion_report')
def parse_symbol_resolution_report(server_msg: ServerMsg | None) -> dict[str, str]:
    res = {
        
        }
    return res