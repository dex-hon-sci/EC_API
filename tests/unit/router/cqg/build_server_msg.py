#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 20:45:59 2026

@author: dexter

"""
from datetime import datetime, timezone
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus


def build_symbol_resolution_report_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    
    symbol_resolution_report = server_msg.information_reports[0].symbol_resolution_report

    symbol_resolution_report.contract_metadata.contract_id = 3
    symbol_resolution_report.contract_metadata.contract_symbol = "CLE"
    symbol_resolution_report.contract_metadata.correct_price_scale = 100
    symbol_resolution_report.contract_metadata.display_price_scale = 200
    symbol_resolution_report.contract_metadata.description = "Desc"
    symbol_resolution_report.contract_metadata.title = "Test CLE title"
    symbol_resolution_report.contract_metadata.tick_size = 10
    symbol_resolution_report.contract_metadata.currency = "USD"
    symbol_resolution_report.contract_metadata.tick_value = 23
    symbol_resolution_report.contract_metadata.cfi_code = "cfi_code"
    symbol_resolution_report.contract_metadata.instrument_group_name = "Crude Oil"
    symbol_resolution_report.contract_metadata.session_info_id = 214
    symbol_resolution_report.contract_metadata.short_instrument_group_name = ""
    symbol_resolution_report.contract_metadata.instrument_group_description = ""
    symbol_resolution_report.contract_metadata.country_code = "AUS"
    return server_msg

def build_session_info_report_server_msg() -> ServerMsg:
    server_msg = ServerMsg()

    information_report = server_msg.information_reports.add()
    information_report.id = 1
    
    session_information_report = server_msg.information_reports[0].session_information_report
    session_information_report.session_info_id = 330
    
    session_segments = session_information_report.session_segments.add()
    session_segments.session_segment_id = 1111
    
    return server_msg
    
def build_historical_orders_report_server_msg() -> ServerMsg:
    TS = datetime.now(timezone.utc)
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    
    historical_orders_report_order_status = information_report.historical_orders_report.order_statuses.add()
    historical_orders_report_order_status.status = OrderStatus.Status.FILLED
    historical_orders_report_order_status.order_id = "1"
    historical_orders_report_order_status.chain_order_id = "A"
    historical_orders_report_order_status.status_utc_timestamp = TS
    historical_orders_report_order_status.fill_cnt = 1
    return server_msg

def build_option_maturity_list_report_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1

    return server_msg

