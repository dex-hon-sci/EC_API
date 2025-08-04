#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 13:07:01 2025

@author: dexter
"""
from EC_API.msg_validation.CQG_connect_enums import (
    LOGON_RESULT_STATUS_ENUMS_BOOL,
    LOGGEDOFF_REASON_ENUMS_BOOL,
    RESTORE_STATUS_ENUMS_BOOL,
    )
from EC_API.msg_validation.CQG_meta_enums import INFORMATION_REPORT_STATUS_ENUMS_BOOL
from EC_API.msg_validation.CQG_trade_enums import (
    TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL,
    NEWORDER_ORDERSTATUS_ENUMS_BOOL,
    MODIFYORDER_ORDERSTATUS_ENUMS_BOOL,
    CANCELORDER_ORDERSTATUS_ENUMS_BOOL,
    ACTIVEATORDER_ORDERSTATUS_ENUMS_BOOL,
    GOFLAT_ORDERSTATUS_ENUMS_BOOL,
    ORDER_REJECT_CODE_ENUMS_BOOL)
from EC_API.msg_validation.CQG_historical_enums import (
    TIMESALES_REPORT_RESULT_ENUMS_BOOL,
    VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL
    )
from EC_API.msg_validation.CQG_market_data_enums import MARKETDATA_SUB_STATUS_ENUMS_BOOL

# Some msg require a status check and some don't
# Matching Status Enums with server_msg types
MAP_STATUS_ENUMS = {"logon_result": LOGON_RESULT_STATUS_ENUMS_BOOL,
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
                    "go_flat_statuses": GOFLAT_ORDERSTATUS_ENUMS_BOOL,
                    "time_and_sales_reports": TIMESALES_REPORT_RESULT_ENUMS_BOOL,
                    "volume_profile_reports": VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL,
                    "market_data_subscription_statuses": MARKETDATA_SUB_STATUS_ENUMS_BOOL,
                    }

# key_value pairs for requests and expected reponse types
MAP_RESPONSES_TYPES_STR = {'logon': ["logon_result",
                                    "concurrent_connection_join_results"],
                          'restore_or_join_session': ["restore_or_join_session_result"],
                          'logoff': ["logged_off"],
                          'ping': ["pong"],
                          'information_requests': ["information_reports"],
                          'trade_subscriptions': ["trade_subscription_statuses",
                                                  "trade_snapshot_completions",
                                                  ],
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


#liquidate_all
#cancel_all_orders
#suspend_order

#position_statuses
#collateral_statuses
#account_summary_statuses


# Information report is_report_complete

# OrderStatus Enum, match OrderID, clorderid

# PositionStatus, CollateralStatus, AccountSummaryStatus, 
# RealTimeMarketData special states
# TimeBarReport state