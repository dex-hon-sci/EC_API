#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 02:39:15 2026

@author: dexter
"""
from typing import Any, Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API._typing import Parser_func
from EC_API.exceptions import MsgParserError

def parse_logon_result(server_msg: ServerMsg | None) -> dict[str, Any]:
    if not server_msg or not server_msg.logon_result:
        raise MsgParserError("Failed to parse logon_result.")
    
    return {
        "result_code": server_msg.logon_result.result_code,
        "base_time": server_msg.logon_result.base_time,
        "server_time": server_msg.logon_result.server_time
        }

def parse_restore_or_join_session_result(server_msg: ServerMsg | None) -> dict[str, Any]:
    if not server_msg or not server_msg.restore_or_join_session_result:
        raise MsgParserError("Failed to parse restore_or_join_session_result.") 

    return {
        "result_code": server_msg.restore_or_join_session_result.result_code,
        "base_time": server_msg.restore_or_join_session_result.base_time,
        "server_time": server_msg.restore_or_join_session_result.server_time
        }
    
def parse_logged_off(server_msg: ServerMsg | None) -> dict[str, Any]: 
    if not server_msg or not server_msg.logged_off:
        raise MsgParserError("Failed to parse logged_off.")

    return {
        "logoff_reason": server_msg.logged_off.logoff_reason,
        }

def parse_pong(server_msg: ServerMsg | None) -> tuple[str, str, int, int]:
    if not server_msg or not server_msg.pong:
        raise MsgParserError("Failed to parse pong.")
    return ("pong", server_msg.pong.token, server_msg.pong.ping_utc_time, 
            server_msg.pong.pong_utc_time)

# --- Metadata parsers ---
metadata_parsers: dict[str, Parser_func] = {}

def register_info_report_parsers(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        metadata_parsers[msg_name] = func
        return func
    return decorator

@register_info_report_parsers('symbol_resoluion_report')
def parse_symbol_resolution_report(
        server_msg: ServerMsg | None
    ) -> list[dict[str, str]]:
    if not server_msg or not server_msg.information_reports:
        raise MsgParserError("Failed to parse information_report.")
    res = []
    information_reports = server_msg.information_reports
    for report in information_reports:
        sym_rp = report.symbol_resolution_report
        temp = {
        'cotract_id': sym_rp.contract_metadata.cotract_id,
        'contract_symbol': sym_rp.contract_metadata.contract_symbol,
        'correct_price_scale': sym_rp.contract_metadata.correct_price_scale,
        'display_price_scale': sym_rp.contract_metadata.display_price_scale,
        'description': sym_rp.contract_metadata.description,
        'title': sym_rp.contract_metadata.title,
        'tick_size': sym_rp.contract_metadata.tick_size,
        'currency': sym_rp.contract_metadata.currency,
        'tick_value': sym_rp.contract_metadata.tick_value,
        'cfi_code': sym_rp.contract_metadata.cfi_code,
        'instrument_group_name': sym_rp.contract_metadata.instrument_group_name,
        'session_info_id': sym_rp.contract_metadata.session_info_id,
        'short_instrument_group_name': sym_rp.contract_metadata.short_instrument_group_name,
        'instrument_group_description': sym_rp.contract_metadata.instrument_group_description,
        'country_code': sym_rp.contract_metadata.country_code         
        }
        res.append(temp)
    return res