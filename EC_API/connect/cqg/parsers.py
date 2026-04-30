#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 02:39:15 2026

@author: dexter
"""
from typing import Any, Callable, Iterable
from google.protobuf.json_format import MessageToDict
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg, InformationReport
from EC_API.protocol.cqg.parser_util import walk_fields
from EC_API._typing import Parser_func
from EC_API.exceptions import MsgParserError

connect_parsers: dict[str, Parser_func] = dict()

def register_parser(name: str):
    def decorator(func: Callable):
        connect_parsers[name] = func
        return func
    return decorator
        
def parse_logon_result(server_msg: ServerMsg) -> dict[str, Any]:
    try: 
        return {
            "result_code": server_msg.logon_result.result_code,
            "base_time": server_msg.logon_result.base_time,
            "server_time": server_msg.logon_result.server_time
            }
    except Exception:
        raise MsgParserError("Failed to parse logon_result.")

def parse_restore_or_join_session_result(server_msg: ServerMsg) -> dict[str, Any]:
    try:
        return {
            "result_code": server_msg.restore_or_join_session_result.result_code,
            "base_time": server_msg.restore_or_join_session_result.base_time,
            "server_time": server_msg.restore_or_join_session_result.server_time
            }
    except Exception:
        raise MsgParserError("Failed to parse restore_or_join_session_result.") 

def parse_logged_off(server_msg: ServerMsg) -> dict[str, Any]: 
    try:
        return {
            "logoff_reason": server_msg.logged_off.logoff_reason,
            }
    except Exception:
        raise MsgParserError("Failed to parse logged_off.")
        
def parse_ping(server_msg: ServerMsg) -> tuple[str, str, int]:
    try:
        return ('ping', server_msg.ping.token, server_msg.ping.ping_utc_time)
    except Exception:
        raise  MsgParserError("Failed to parse ping.")

def parse_pong(server_msg: ServerMsg) -> tuple[str, str, int, int]:
    try:
        return ("pong", server_msg.pong.token, server_msg.pong.ping_utc_time, 
                server_msg.pong.pong_utc_time)
    except Exception:
        raise MsgParserError("Failed to parse pong.")

# --- Metadata parsers ---
# Special Treatment for Metadata. For CQG, all metadata are sub-messages in
# information_reports. Hence after server_msg going through parse_server_msg()
# using the server_msg_type(): "information_reports", we have to route it through
# yet another master parser function: parse_information_report()
metadata_parsers: dict[str, Parser_func] = {}

def register_info_report_parsers(msg_name: str):
    # decorator for registering extractors functions
    def decorator(func: Callable[..., None]):
        metadata_parsers[msg_name] = func
        return func
    return decorator
    
# --- parse metadat
@register_parser('information_reports')
def parse_information_report(        
        server_msg: ServerMsg,
    ) -> list[dict[str, str]]:
    
    INFO_SUBTYPE = set(metadata_parsers.keys())
    
    def selector(fd, val) -> Iterable[str]:
        if fd.name in INFO_SUBTYPE:
            yield fd.name
    
    res = []
    information_reports = server_msg.information_reports
    for report in information_reports:
        
        # walk and get types
        info_subtype_name = walk_fields(report, selector, max_depth = 1)
        for name in info_subtype_name:
            p_rp: dict[str, Any] = metadata_parsers[name](report)
            p_rp['id'] = report.id
            p_rp['status_code'] = report.status_code
            res.append(p_rp)

    return res

# --- specific parsers for info reports
@register_info_report_parsers('symbol_resolution_report')
def parse_symbol_resolution_report(
        report: InformationReport
    ) -> dict[str, str]:
    try:
        return MessageToDict(
            report.symbol_resolution_report,
              preserving_proto_field_name=True
            )
    except Exception:
        raise MsgParserError("Failed to parse symbol_resolution_report.")

@register_info_report_parsers('session_information_report')
def parse_session_information_report(
        report: InformationReport
    ) -> dict[str, str]:
    try:
        return MessageToDict(
              report.session_information_report,
              preserving_proto_field_name=True
          )
    except Exception:
        raise MsgParserError("Failed to parse session_information_report.")

@register_info_report_parsers('historical_orders_report')
def parse_historical_orders_report(
        report: InformationReport
    ) -> list[dict[str, str]]:
    
    try:
        return MessageToDict(
              report.historical_orders_report,
              preserving_proto_field_name=True
            )
    except Exception:
        raise MsgParserError("Failed to parse historical_orders_report.")


@register_info_report_parsers('option_maturity_list_report')
def parse_option_maturity_list_report(
        report: InformationReport
    ) -> list[dict[str, str]]:
    try:
        return MessageToDict(
              report.option_maturity_list_report,
              preserving_proto_field_name=True
            )
    except Exception:
        raise MsgParserError("Failed to parse option_maturity_list_report.")

@register_info_report_parsers('instrument_group_report')
def parse_instrument_group_report(
        report: InformationReport
    ) -> list[dict[str, str]]:
    try:
        return MessageToDict(
              report.instrument_group_report,
              preserving_proto_field_name=True
            )
    except Exception:
        raise MsgParserError("Failed to parse instrument_group_report.")

@register_info_report_parsers('at_the_money_strike_report')
def parse_at_the_money_strike_report(
        report: InformationReport
    ) -> list[dict[str, str]]:
    try:
        return MessageToDict(
              report.at_the_money_strike_report,
              preserving_proto_field_name=True
            )
    except Exception:
        raise MsgParserError("Failed to parse at_the_money_strike_report.")
# =============================================================================
#         return {
#         'contract_id': sym_rp.contract_metadata.contract_id,
#         'contract_symbol': sym_rp.contract_metadata.contract_symbol,
#         'correct_price_scale': sym_rp.contract_metadata.correct_price_scale,
#         'display_price_scale': sym_rp.contract_metadata.display_price_scale,
#         'description': sym_rp.contract_metadata.description,
#         'title': sym_rp.contract_metadata.title,
#         'tick_size': sym_rp.contract_metadata.tick_size,
#         'currency': sym_rp.contract_metadata.currency,
#         'tick_value': sym_rp.contract_metadata.tick_value,
#         'cfi_code': sym_rp.contract_metadata.cfi_code,
#         'instrument_group_name': sym_rp.contract_metadata.instrument_group_name,
#         'session_info_id': sym_rp.contract_metadata.session_info_id,
#         'short_instrument_group_name': sym_rp.contract_metadata.short_instrument_group_name,
#         'instrument_group_description': sym_rp.contract_metadata.instrument_group_description,
#         'country_code': sym_rp.contract_metadata.country_code         
#         }
#     except Exception:
# =============================================================================
