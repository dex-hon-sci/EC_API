#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 20:45:59 2026

@author: dexter

"""
from datetime import datetime, timezone
from decimal import Decimal
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus, TransactionStatus
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LgRes
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as RstJoinSessRes
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LgOff
from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as InfoRp
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as TrsSub
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus as TrdSubStatus
from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus as GFltStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as MktDSub
from EC_API.ext.WebAPI.market_data_2_pb2 import Quote
from EC_API.ext.WebAPI.historical_2_pb2 import TimeAndSalesReport as TSrRep
from EC_API.ext.WebAPI.historical_2_pb2 import BarReportStatusCode as BarRpStatusCode
from EC_API.ext.WebAPI.historical_2_pb2 import VolumeProfileReport as VolPrfRep
### ---- Connection ----
# (1) logon_result (v)
# (2) restore_or_join_session_result (v)
# (3) concurrent_connection_join_results (v)
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
    logon_result.protocol_version_minor = 101
    logon_result.protocol_version_major = 202
    logon_result.server_time = int(datetime.now().timestamp())
    return server_msg
    
def build_restore_or_join_session_result_server_msg(
        res_code: RstJoinSessRes.ResultCode
    ) -> ServerMsg:
    server_msg = ServerMsg()

    restore_or_join_session_result = server_msg.restore_or_join_session_result
    
    restore_or_join_session_result.result_code = res_code
    restore_or_join_session_result.base_time = datetime.now().isoformat()
    restore_or_join_session_result.server_time = int(datetime.now().timestamp())
    return server_msg

def build_concurrent_connection_join_results_server_msg(
        res: bool
    ) -> ServerMsg:  
    server_msg = ServerMsg()

    concurrent_connection_join_results = server_msg.concurrent_connection_join_results.add()
    concurrent_connection_join_results.is_same_app_type = res
    return server_msg

def build_logged_off_server_msg(
        res: LgOff.LogoffReason
    ) -> ServerMsg:
    server_msg = ServerMsg()
    logged_off = server_msg.logged_off
    logged_off.logoff_reason = res
    return server_msg

def build_pong_server_msg(
        ping_time: int,
        delay: int 
    ) -> ServerMsg:
    server_msg = ServerMsg()
    pong = server_msg.pong
    pong.ping_utc_time= ping_time
    pong.pong_utc_time = ping_time + delay
    return server_msg

### ---- information_report ----
# accounts_report
# (1) symbol_resolution_report (v)
# last_statement_balances_report
# currency_rates_report
# (2) session_information_report (v)
# (3) historical_orders_request (v)
# (4) option_maturity_list_report (v)
# (5) instrument_group_report (v)
# (6) at_the_money_strike_report (v)
# symbol_list_report
# symbol_report
# account_risk_parameters_report
# order_status_report
def build_symbol_resolution_report_server_msg(
        res = InfoRp.StatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res
    
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

def build_session_info_report_server_msg(
        res: InfoRp.StatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()

    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res

    session_information_report = server_msg.information_reports[0].session_information_report
    session_information_report.session_info_id = 330
    
    session_segments = session_information_report.session_segments.add()
    session_segments.session_segment_id = 1111
    
    return server_msg
    
def build_historical_orders_report_server_msg(
        res: InfoRp.StatusCode
    ) -> ServerMsg:
    TS = datetime.now(timezone.utc)
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res

    historical_orders_report_order_status = information_report.historical_orders_report.order_statuses.add()
    historical_orders_report_order_status.status = OrderStatus.Status.FILLED
    historical_orders_report_order_status.order_id = "1"
    historical_orders_report_order_status.chain_order_id = "A"
    historical_orders_report_order_status.status_utc_timestamp = TS
    historical_orders_report_order_status.fill_cnt = 1
    return server_msg

def build_option_maturity_list_report_server_msg(
        res: InfoRp.StatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res

    option_maturities = information_report.option_maturity_list_report.option_maturities.add()
    option_maturities.id = "id_1"
    option_maturities.name = "CLXXXX"
    option_maturities.description = "description"
    return server_msg

def build_instrument_group_report_server_msg(
        res: InfoRp.StatusCode
    ) -> ServerMsg: 
    server_msg = ServerMsg()
    
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res

    instruments = information_report.instrument_group_report.instruments.add()
    instruments.id = "id_1"
    instruments.name = "Instrument_1"
    instruments.description = "description"
    return server_msg

def build_at_the_money_strike_report_server_msg(
        res: InfoRp.StatusCode
    ) -> ServerMsg: 
    server_msg = ServerMsg()
    information_report = server_msg.information_reports.add()
    information_report.id = 1
    information_report.status_code = res

    at_the_money_strike_report = information_report.at_the_money_strike_report
    at_the_money_strike_report.strike =100
    return server_msg
    
### ---- Orders----
# (1) order_request_rejects (v)
# (2) order_request_acks (v)
# (3) trade_subscription_statuses (v)
# (4) trade_snapshot_completions (v)
# (5) order_statuses (v)
# (6) position_statuses (v)
# (7) account_summary_statuses (v)
# (8) go_flat_statuses (v)
def build_order_request_rejects_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    
    order_request_rejects = server_msg.order_request_rejects.add()
    order_request_rejects.request_id = 1
    order_request_rejects.reject_code = 1001
    
    return server_msg

def build_order_request_acks_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    
    order_request_acks = server_msg.order_request_acks.add()
    order_request_acks.request_id = 1
    order_request_acks.when = datetime.now()
    return server_msg

def build_trade_subscription_statuses_server_msg(res: TrdSubStatus.StatusCode) -> ServerMsg:
    server_msg = ServerMsg()
    trade_subscription_statuses = server_msg.trade_subscription_statuses.add()
    trade_subscription_statuses.id = 1
    
    trade_subscription_statuses.status_code = res
    return server_msg


def build_trade_snapshot_completetions_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    trade_snapshot_completions = server_msg.trade_snapshot_completions.add()
    
    trade_snapshot_completions.subscription_id = 1
    
    sub_scope = trade_snapshot_completions.subscription_scopes
    sub_scope.append(TrsSub.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS)
    sub_scope.append(TrsSub.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS)
    sub_scope.append(TrsSub.SubscriptionScope.SUBSCRIPTION_SCOPE_COLLATERAL)
    sub_scope.append(TrsSub.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY)
    return server_msg

def build_order_statuses_server_msg(
        res: OrderStatus.Status = OrderStatus.Status.IN_TRANSIT
    ) -> ServerMsg:
    server_msg = ServerMsg()
    
    order_statuses = server_msg.order_statuses.add()
    
    # ----
    order_statuses.subscription_ids.append(1)
    order_statuses.status = res
    order_statuses.order_id = "order_id_1"
    order_statuses.chain_order_id = "chain_order_id_1"
    order_statuses.status_utc_timestamp = datetime.now()
    order_statuses.submission_utc_timestamp = datetime.now()
    order_statuses.fill_cnt = 0
    order_statuses.scaled_avg_fill_price = -200
    order_statuses.avg_fill_price_correct = 10
    #----
    transaction_statuses = order_statuses.transaction_statuses.add()
    transaction_statuses.status = TransactionStatus.Status.IN_TRANSIT
    transaction_statuses.trans_id = 2
    transaction_statuses.trans_utc_timestamp = datetime.now()
    transaction_statuses.cl_order_id = "cl_order_id_1"
    
    trades = transaction_statuses.trades.add()
    trades.trade_id = "trade_id_1"
    trades.contract_id = 0
    trades.statement_date = int(datetime.now().timestamp())
    trades.trade_utc_timestamp = datetime.now()
    
    trades.scaled_price = 1000 #price = round(price_correct / correct_price_scale)
    trades.price_correct = 100100
    trades.side = Ord.Side.SIDE_BUY
    # ----
    order_statuses.entered_by_user = "user_A"
    order_statuses.first_statement_date = int(datetime.now().timestamp())
    # ----
    contract_metadata = order_statuses.contract_metadata.add()
    contract_metadata.contract_id = 0
    contract_metadata.contract_symbol = "Symbol_1"
    contract_metadata.correct_price_scale = 0.01
    contract_metadata.display_price_scale = 202
    contract_metadata.description = "description"
    contract_metadata.title = "title"
    contract_metadata.tick_size = 10
    contract_metadata.currency = "USD"
    contract_metadata.tick_value = 0
    contract_metadata.cfi_code = "ESVUFB"
    contract_metadata.instrument_group_name = "instru_group_1"
    contract_metadata.session_info_id  = 232323
    contract_metadata.short_instrument_group_name = "short_instrument_group_name"
    contract_metadata.instrument_group_description = "instrument_group_description"
    contract_metadata.country_code = "US"
    # ----
    order_statuses.account_id = 123466    
    return server_msg


def build_position_statuses_server_msg() -> ServerMsg:    
    server_msg = ServerMsg()
    
    position_statuses = server_msg.position_statuses.add()
    position_statuses.subscription_ids.append(0)
    position_statuses.subscription_ids.append(1)
    position_statuses.subscription_ids.append(2)
    
    position_statuses.account_id = 123466
    position_statuses.contract_id = 0 
    position_statuses.is_short_open_position = False
    # ----
    open_positions = position_statuses.open_positions.add()
    open_positions.id = 2
    open_positions.price_correct = 101
    open_positions.trade_date = int(datetime.now().timestamp())
    open_positions.statement_date = int(datetime.now().timestamp())
    open_positions.is_aggregated = True
    open_positions.is_short = False
    
    # ----
    purchase_and_sales_groups = position_statuses.purchase_and_sales_groups.add()
    purchase_and_sales_groups.id = 4
    purchase_and_sales_groups.realized_profit_loss = 10
    
    matched_trades = purchase_and_sales_groups.matched_trades.add()
    matched_trades.price = 292
    matched_trades.trade_date = int(datetime.now().timestamp())
    matched_trades.statement_date = int(datetime.now().timestamp())
    matched_trades.is_aggregated = True
    # ----
    today_fill_commissions = position_statuses.today_fill_commissions.add()
    today_fill_commissions.commission_currency = "USD"
    today_fill_commissions.commission = 102
    return server_msg


def build_account_summary_statuses_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    account_summary_statuses = server_msg.account_summary_statuses.add()
    account_summary_statuses.subscription_ids.append(1)
    account_summary_statuses.subscription_ids.append(2)
    account_summary_statuses.subscription_ids.append(3)
    
    account_summary_statuses.account_id = 1210221
    account_summary_statuses.currency = "USD"
    account_summary_statuses.purchasing_power = 1_000_000
    
    return server_msg


def build_go_flat_statuses_server_msg(
        res: GFltStatus.StatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    
    go_flat_statuses = server_msg.go_flat_statuses.add()
    go_flat_statuses.request_id = 1 
    go_flat_statuses.account_id = 1210221
    go_flat_statuses.status_code = res
    
    return server_msg

### ---- Market Data ----
# (1) market_data_subscription_statuses (v)
# (2) real_time_market_data (v)
def build_market_data_subscription_statuses_server_msg(
        res: MktDSubStatus.StatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    market_data_subscription_statuses = server_msg.market_data_subscription_statuses.add()
    market_data_subscription_statuses.contract_id = 1
    market_data_subscription_statuses.status_code = res
    
    market_data_subscription_statuses.level = MktDSub.Level.LEVEL_TRADES
        
    return server_msg


def build_real_time_market_data_server_msg() -> ServerMsg:
    server_msg = ServerMsg()
    real_time_market_data = server_msg.real_time_market_data.add()
    
    real_time_market_data.contract_id = 1
    
    # ----
    quotes = real_time_market_data.quotes.add()
    quotes.quote_utc_time = int(datetime.now().timestamp())
    quotes.type = Quote.Type.TYPE_TRADE
    quotes.scaled_price = 19201
    quotes.scaled_source_price = 10029
    #quotes.volume = 200
    quotes.indicators.append(Quote.Indicator.INDICATOR_OPEN)
    quotes.sales_condition = Quote.SalesCondition.SALES_CONDITION_HIT
    
    # ----
    market_values = real_time_market_data.market_values.add()
    
    market_values.scaled_open_price = 19600
    market_values.scaled_high_price = 20331
    market_values.scaled_low_price = 18890
    market_values.scaled_close_price = 19202
    market_values.total_volume.significand = 12
    
    # ----
    quotes1 = real_time_market_data.quotes.add()
    quotes1.quote_utc_time = int(datetime.now().timestamp())
    quotes1.type = Quote.Type.TYPE_TRADE
    quotes1.scaled_price = 1400
    quotes1.scaled_source_price = 129
    #quotes1.volume = 200
    quotes1.indicators.append(Quote.Indicator.INDICATOR_OPEN)
    quotes1.sales_condition = Quote.SalesCondition.SALES_CONDITION_HIT
    
    # ----
    market_values1 = real_time_market_data.market_values.add()
    
    market_values1.scaled_open_price = 786
    market_values1.scaled_high_price = 890
    market_values1.scaled_low_price = 611
    market_values1.scaled_close_price = 755
    market_values.total_volume.significand = 16

    return server_msg


## Historical Data
# (1) time_and_sales_reports (v)
# (2) time_bar_reports (v)
# (3) volume_profile_reports (v)
# (4) non_timed_bar_reports (v)
def build_time_and_sales_reports_server_msg(
        res: TSrRep.ResultCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    time_and_sales_reports = server_msg.time_and_sales_reports.add()
    
    time_and_sales_reports.request_id = 1
    time_and_sales_reports.result_code = res
    
    quotes = time_and_sales_reports.quotes.add()
    quotes.quote_utc_time = int(datetime.now().timestamp())
    quotes.type = Quote.Type.TYPE_TRADE
    quotes.scaled_price = 121
    quotes.scaled_source_price = 464
    quotes.volume.significand = 200
    quotes.indicators.append(Quote.Indicator.INDICATOR_OPEN)
    quotes.sales_condition = Quote.SalesCondition.SALES_CONDITION_HIT

    return server_msg

def build_time_bar_reports_server_msg(
        res: BarRpStatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    time_bar_reports = server_msg.time_bar_reports.add()
    
    time_bar_reports.request_id = 1
    time_bar_reports.status_code = res
    
    time_bars = time_bar_reports.time_bars.add()
    time_bars.bar_utc_time = int(datetime.now().timestamp())
    time_bars.scaled_open_price = 987
    time_bars.scaled_high_price = 1241
    time_bars.scaled_low_price = 902
    time_bars.scaled_close_price = 1002
    
    time_bars.volume.significand = 19
    return server_msg

def build_volume_profile_reports_server_msg(
        res: VolPrfRep.ResultCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    volume_profile_reports = server_msg.volume_profile_reports.add()
    
    volume_profile_reports.request_id = 1
    volume_profile_reports.result_code = res
    
    volume_profile_items = volume_profile_reports.volume_profile_items.add()
    volume_profile_items.scaled_price = 67541
    volume_profile_items.volume.significand = 12
    volume_profile_items.ask_volume.significand = 2
    volume_profile_items.bid_volume.significand = 5
    volume_profile_items.tick_volume = 1
    volume_profile_items.ask_tick_volume.significand = 7
    volume_profile_items.bid_tick_volume.significand = 6
    return server_msg

def build_non_timed_bar_reports_server_msg(
        res: BarRpStatusCode
    ) -> ServerMsg:
    server_msg = ServerMsg()
    non_timed_bar_reports = server_msg.non_timed_bar_reports.add()
    
    non_timed_bar_reports.request_id = 1
    non_timed_bar_reports.status_code = res
    # add more later
    return server_msg


