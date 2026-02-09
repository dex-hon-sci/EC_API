#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 20:45:59 2026

@author: dexter

"""
from datetime import datetime, timezone
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LgRes
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as RstJoinSessRes
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LgOff
### ---- Connection ----
# (1) logon_result (v)
# (2) restore_or_join_session_result (v)
# (3) logged_off (v)
# (4) pong (v)
###LgRes.ResultCode.RESULT_CODE_SUCCESS
def build_logon_result_server_msg(
        res_code: LgRes.ResultCode
    ) -> ServerMsg:
    server_msg = ServerMsg()

    logon_result = server_msg.logon_result
    
    logon_result.result_code = res_code
    logon_result.base_time = datetime.now().isoformat()
    logon_result.protocol_version_minor = "protocol_ver_test_minor_101"
    logon_result.protocol_version_major = "protocol_ver_test_major_202"
    logon_result.server_time = int(datetime.now().timestamp())
    
def build_restore_or_join_session_result_server_msg(
        res_code: RstJoinSessRes
    ) -> ServerMsg:
    server_msg = ServerMsg()

    restore_or_join_session_result = server_msg.restore_or_join_session_result
    
    restore_or_join_session_result.result_code = res_code
    restore_or_join_session_result.base_time = datetime.now().isoformat()
    restore_or_join_session_result.server_time = int(datetime.now().timestamp())
    
def build_concurrent_connection_join_results_server_msg(
        res: bool
    ) -> ServerMsg:  
    server_msg = ServerMsg()

    concurrent_connection_join_results = server_msg.concurrent_connection_join_results
    concurrent_connection_join_results.is_same_app_type = res
    
def build_logged_off_server_msg(
        res: LgOff.LogoffReason
    ) -> ServerMsg:
    server_msg = ServerMsg()
    logged_off = server_msg.logged_off
    logged_off.logoff_reason = res
    
def build_pong_server_msg(
        ping_time: int,
        delay: int 
    ) -> ServerMsg:
    server_msg = ServerMsg()
    pong = server_msg.pong
    pong.ping_utc_time= ping_time
    pong.pong_utc_time = ping_time + delay
    
### ---- information_report ----
# accounts_report
# symbol_resolution_report (v)
# session_information_report (v)
# historical_orders_request (v)
# option_maturity_list_report
# instrument_group_report
# at_the_money_strike_report
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

def build_instrument_group_report_server_msg() -> ServerMsg: ...

def build_at_the_money_strike_report_server_msg() -> ServerMsg: ...

### ---- Orders----
# order_request_rejects
# order_request_acks
# trade_subscription_statuses
# trade_snapshot_completions
# order_statuses
# position_statuses
# account_summary_statuses
# go_flat_statuses
def build_order_request_rejects_server_msg() -> ServerMsg:...

def build_order_request_acks_server_msg() -> ServerMsg:...

def build_trade_subscription_statuses_server_msg() -> ServerMsg:...

def build_trade_snapshot_completetions_server_msg() -> ServerMsg:...

def build_order_statuses_server_msg() -> ServerMsg:...

def build_position_statuses_server_msg() -> ServerMsg:...

def build_account_summary_statuses_server_msg() -> ServerMsg:...

def build_go_flat_statuses_server_msg() -> ServerMsg:...

### ---- Market Data ----
# market_data_subscription_statuses
# real_time_market_data
def build_market_data_subscription_statuses_server_msg() -> ServerMsg:...

def build_real_time_market_data_server_msg() -> ServerMsg:...


## Historical Data
# time_and_sales_reports
# time_bar_reports
# volume_profile_reports
# non_timed_bar_reports
def build_time_and_sales_reports_server_msg() -> ServerMsg: ...
def build_time_bar_reports_server_msg() -> ServerMsg: ...
def build_volume_profile_reports_server_msg() -> ServerMsg: ...
def build_non_timed_bar_reports_server_msg() -> ServerMsg: ...


