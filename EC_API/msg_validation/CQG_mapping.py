#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 13:07:01 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

from EC_API.msg_validation.CQG_connect_enums import (
    LOGON_RESULT_STATUS_ENUMS_BOOL,
    LOGGEDOFF_REASON_ENUMS_BOOL,
    RESTORE_STATUS_ENUMS_BOOL,
    )
from EC_API.msg_validation.CQG_trade_enums import (
    TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL,
    NEWORDER_ORDERSTATUS_ENUMS_BOOL,
    MODIFYORDER_ORDERSTATUS_ENUMS_BOOL,
    CANCELORDER_ORDERSTATUS_ENUMS_BOOL,
    ACTIVEATORDER_ORDERSTATUS_ENUMS_BOOL,
    GOFLAT_ORDERSTATUS_ENUMS_BOOL,
    ORDER_REJECT_CODE_ENUMS_BOOL
    )
from EC_API.msg_validation.CQG_historical_enums import (
    TIMESALES_REPORT_RESULT_ENUMS_BOOL,
    VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL
    )
from EC_API.msg_validation.CQG_meta_enums import (
    INFORMATION_REPORT_STATUS_ENUMS_BOOL
    )
from EC_API.msg_validation.CQG_market_data_enums import (
    MARKETDATA_SUB_STATUS_ENUMS_BOOL
    )

# Some msg require a status check and some don't
# Matching Status Enums with server_msg types
MAP_STATUS_ENUMS = {
    "logon_result": LOGON_RESULT_STATUS_ENUMS_BOOL,
    "logged_off": LOGGEDOFF_REASON_ENUMS_BOOL,
    "restore_or_join_session_result": RESTORE_STATUS_ENUMS_BOOL,
    "information_reprort": INFORMATION_REPORT_STATUS_ENUMS_BOOL,
    "trade_subscription_statuses": TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL,
    "order_request_rejects": ORDER_REJECT_CODE_ENUMS_BOOL,
    "order_statuses": {"new_order": NEWORDER_ORDERSTATUS_ENUMS_BOOL,
                       "modify_order": MODIFYORDER_ORDERSTATUS_ENUMS_BOOL,
                       "cancel_order": CANCELORDER_ORDERSTATUS_ENUMS_BOOL,
                       "activate_order":ACTIVEATORDER_ORDERSTATUS_ENUMS_BOOL,
                       "go_flat": GOFLAT_ORDERSTATUS_ENUMS_BOOL,
                       },
    "position_statuses": {},
    "collateral_statuses": {},
    "account_summary_statuses": {},
    "go_flat_statuses": GOFLAT_ORDERSTATUS_ENUMS_BOOL,
    "time_and_sales_reports": TIMESALES_REPORT_RESULT_ENUMS_BOOL,
    "volume_profile_reports": VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL,
    "market_data_subscription_statuses": MARKETDATA_SUB_STATUS_ENUMS_BOOL,
    }

# key_value pairs for requests and expected reponse types
MAP_RESPONSES_TYPES_STR = {
    'logon': ["logon_result", "concurrent_connection_join_results"],
    'restore_or_join_session': ["restore_or_join_session_result"],
    'logoff': ["logged_off"],
    'ping': ["pong"],
    'information_requests': ["information_reports"],
    'trade_subscriptions': ["trade_subscription_statuses",
                            "trade_snapshot_completions",],
    'order_requests': ["order_statuses", 
                       "go_flat_statuses",
                       "order_request_rejects",
                       "order_request_acks"],
    'market_data_subscriptions': ["market_data_subscription_statuses",
                                  "real_time_market_data"],
    'time_and_sales_requests': ["time_and_sales_reports"],
    'time_bar_requests': ["time_bar_reports"],
    'volume_profile_requests': ["volume_profile_reports"],
    'non_timed_bar_requests': ["non_timed_bar_reports"]
    }

def extract_result_code_from_server_msg(server_msg: ServerMsg, 
                                        keyword: str) -> int:
    MAP_RESULT_CODE = {
        "logon_result": server_msg.result_code,
        "logged_off": server_msg.logoff_reason,
        "restore_or_join_session_result": server_msg.result_code,
        "information_reprort": server_msg.status_code,
        "trade_subscription_statuses": server_msg.status_code,
        "order_request_rejects": server_msg.reject_code,
        "order_statuses": {"new_order": 0,
                            "modify_order": 0,
                            "cancel_order": 0,
                            "activate_order":0,
                            "go_flat": 0,
                            },
        "position_statuses": {},
        "collateral_statuses": {},
        "account_summary_statuses": {},
        "go_flat_statuses": server_msg.status_code,
        "time_and_sales_reports": server_msg.result_code,
        "volume_profile_reports": server_msg.result_code,
        "market_data_subscription_statuses": server_msg.result_code,
                       }
    
    if keyword in list(MAP_RESULT_CODE.keys()):
        return MAP_RESULT_CODE[keyword]


def extract_special_clear_from_server_msg(server_msg: ServerMsg, 
                                          keyword: str) -> bool:
    # Check for special conditions
    MAP_SPECIAL_CLEAR = {
        "information_requests": (server_msg.is_report_complete is True),
        "trade_subscriptions": (server_msg.trade_snapshot_completions is not None),
        "new_order": (server_msg.order_request_rejects is not None),
        "modify_order": (server_msg.order_request_rejects is not None),
        "cancel_order": (server_msg.order_request_rejects is not None),
        "activate_order": (server_msg.order_request_rejects is not None),
                         }
    if keyword in list(MAP_SPECIAL_CLEAR.keys()):
        return MAP_SPECIAL_CLEAR[keyword]
    else: 
    # If special conditions does not exist, assume no special clear is needed
        return True

def extract_IDs_from_client_msg(client_msg: ClientMsg,
                                keyword: str) -> dict:
    MAP_MSG_ID_code = {
        "information_reprort": msg.id,
        "trade_subscriptions": msg.id,
        "order_requests": {"new_order": msg.id,
                            "modify_order": 0,
                            "cancel_order": 0,
                            "activate_order":0,
                            "go_flat": 0,
                            },
        "time_and_sales_requests": msg.id,
        "volume_profile_requests": msg.id,
        "non_timed_bar_requests": msg.id,
                       }

    return 
def extract_IDs_from_server_msg(server_msg: ServerMsg,
                                keyword: str) -> dict:
    MAP_MSG_ID_code = {
        "information_requests": msg.id,
        "trade_subscription_statuses": msg.id,
        "order_request_rejects": msg.id,
        "order_statuses": {"new_order": msg.id,
                            "modify_order": 0,
                            "cancel_order": 0,
                            "activate_order":0,
                            "go_flat": 0,
                            },
        "position_statuses": {},
        "collateral_statuses": {},
        "account_summary_statuses": {},
        "go_flat_statuses": msg.id,
        "time_and_sales_reports": msg.id,
        "volume_profile_reports": msg.id,
        "market_data_subscription_statuses": msg.id,
                       }

    return 
        

#liquidate_all
#cancel_all_orders
#suspend_order

# PositionStatus, CollateralStatus, AccountSummaryStatus, 
# RealTimeMarketData special states
# TimeBarReport state