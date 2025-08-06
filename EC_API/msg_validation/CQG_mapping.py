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
                       "order_request_acks",
                       "position_statuses",
                       "collateral_statuses",
                       "account_summary_statuses"
                       ],
    'market_data_subscriptions': ["market_data_subscription_statuses",
                                  "real_time_market_data"],
    'time_and_sales_requests': ["time_and_sales_reports"],
    'time_bar_requests': ["time_bar_reports"],
    'volume_profile_requests': ["volume_profile_reports"],
    'non_timed_bar_requests': ["non_timed_bar_reports"]
    }

def find_order_request_type()->str:
    # For Order_request type either new_order, modify_order, cancel_order,...
    return 

def find_order_status_type(server_msg:ServerMsg)->str:
    # For Order_statues
    Q = {"new_order": {"request_id": server_msg.order_statuses.request_id,
                      "contract_id": server_msg.order_statues.order.contract_id,
                      "cl_order_id": server_msg.order_statues.order.cl_order_id
                      },
        "modify_order": {"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.order_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id,
                        },
        "cancel_order": {"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.order_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id
                         },
        "activate_order":{"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.contract_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id
                         },}
    return 


def map_result_code_client2server_msg(server_msg: ServerMsg, 
                                      keyword: str) -> int:
    MAP_RESULT_CODE = {
        "logon_result": server_msg.result_code,
        "logged_off": server_msg.logoff_reason,
        "restore_or_join_session_result": server_msg.result_code,
        "information_reprort": server_msg.status_code,
        "trade_subscription_statuses": server_msg.status_code,
        "order_request_rejects": server_msg.reject_code,
        "order_statuses": server_msg.status,
        "go_flat_statuses": server_msg.status,
        "time_and_sales_reports": server_msg.result_code,
        "volume_profile_reports": server_msg.result_code,
        "market_data_subscription_statuses": server_msg.result_code,
        }
    
    if keyword in list(MAP_RESULT_CODE.keys()):
        return MAP_RESULT_CODE[keyword]


def map_special_clear_client2server_msg(server_msg: ServerMsg, 
                                          keyword: str) -> bool:
    # Pair client msg (keys) with special conditions (values) in server msg
    # Check for special conditions
    MAP_SPECIAL_CLEAR = {
        "information_requests": (server_msg.is_report_complete is True),
        "trade_subscriptions": (server_msg.trade_snapshot_completions is not None),
        "new_order": (server_msg.order_request_rejects is not None),
        "modify_order": (server_msg.order_request_rejects is not None),
        "cancel_order": (server_msg.order_request_rejects is not None),
        "activate_order": (server_msg.order_request_rejects is not None),
        "goflat_order": (server_msg.order_request_rejects is not None)
        }
    
    if keyword in list(MAP_SPECIAL_CLEAR.keys()):
        return MAP_SPECIAL_CLEAR[keyword]
    else: 
        # If special conditions does not exist, assume no special clear is needed
        return True

def extract_IDs_from_client_msg(client_msg: ClientMsg,
                                keyword: str) -> dict:
    MAP_MSG_ID_code = {
        "information_requests": client_msg.id,
        "trade_subscriptions": client_msg.id,
        "order_requests": {
            "new_order": {"request_id": client_msg.request_id,
                          "contract_id": client_msg.new_order.order.contract_id,
                          "cl_order_id": client_msg.new_order.order.cl_order_id
                         },
            "modify_order": {"request_id": client_msg.modify_order.request_id,
                             "order_id": client_msg.modify_order.order_id,
                             "cl_order_id": client_msg.modify_order.cl_order_id,
                             "orig_cl_order_id": client_msg.modify_order.orig_cl_order_id
                             },
            "cancel_order": {"request_id": client_msg.cancel_order.request_id,
                             "order_id": client_msg.cancel_order.order_id,
                             "cl_order_id": client_msg.cancel_order.cl_order_id,
                             "orig_cl_order_id": client_msg.cancel_order.orig_cl_order_id
                             },
            "activate_order":{"request_id": client_msg.activate_order.request_id,
                             "order_id": client_msg.activate_order.contract_id,
                             "cl_order_id": client_msg.activate_order.cl_order_id,
                             "orig_cl_order_id": client_msg.activate_order.orig_cl_order_id
                             },
            "go_flat": {"request_id": client_msg.request_id,},
            },
        
        "time_and_sales_requests": client_msg.request_id,
        "volume_profile_requests": client_msg.request_id,
        "non_timed_bar_requests": client_msg.request_id,
        }

    return MAP_MSG_ID_code[keyword]

def extract_IDs_from_server_msg(server_msg: ServerMsg,
                                keyword: str) -> dict:
    MAP_MSG_ID_code = {
        "information_report": server_msg.id,
        "trade_subscription_statuses": server_msg.id,
        "order_request_rejects": server_msg.request_id,
        "new_order": {"request_id": server_msg.order_statuses.request_id,
                      "contract_id": server_msg.order_statues.order.contract_id,
                      "cl_order_id": server_msg.order_statues.order.cl_order_id
                      },
        "modify_order": {"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.order_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id,
                        },
        "cancel_order": {"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.order_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id
                         },
        "activate_order":{"request_id": server_msg.order_statuses.request_id,
                         "order_id": server_msg.order_statuses.contract_id,
                         "cl_order_id": server_msg.order_statuses.cl_order_id,
                         "orig_cl_order_id": server_msg.order_statuses.order.cl_order_id
                         },
        "go_flat_statuses": server_msg.request_id,
        "time_and_sales_reports": server_msg.request_id,
        "volume_profile_reports": server_msg.request_id,
        "market_data_subscription_statuses": server_msg.request_id
        }
    
    ORDER_STATUS_ID = {"order_statuses": {}}
    MAP_MSG_ID_code = dict(MAP_MSG_ID_code, **ORDER_STATUS_ID)

    return MAP_MSG_ID_code[keyword]
        

#liquidate_all
#cancel_all_orders
#suspend_order

# PositionStatus, CollateralStatus, AccountSummaryStatus, 
# RealTimeMarketData special states
# TimeBarReport state