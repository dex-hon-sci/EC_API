#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 13:07:01 2025

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LOR
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LOff
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as Restore

LOGON_RESULT_STATUS_ENUMS_BOOL = {
    "Accept": [LOR.ResultCode.RESULT_CODE_SUCCESS] ,
    "Reject": [LOR.ResultCode.RESULT_CODE_FAILURE,
              LOR.ResultCode.RESULT_CODE_NO_ONETIME_PASSWORD,
              LOR.ResultCode.RESULT_CODE_PASSWORD_EXPIRED,
              LOR.ResultCode.RESULT_CODE_CONCURRENT_SESSION,
              LOR.ResultCode.RESULT_CODE_REDIRECTED,
              LOR.ResultCode.RESULT_CODE_ROUTINE_ERROR,
              LOR.ResultCode.RESULT_CODE_ACCESS_TOKEN_EXPIRED
              ]
    }

LOGGEDOFF_REASON_ENUMS_BOOL = {
    "Accept": [LOff.LogoffReason.LOGOFF_REASON_BY_REQUEST,
               LOff.LogoffReason.LOGOFF_REASON_REDIRECTED,
               LOff.LogoffReason.LOGOFF_REASON_FORCED,
               LOff.LogoffReason.LOGOFF_REASON_REASSIGNED
               ],
    "Reject": []
    }

RESTORE_STATUS_ENUMS_BOOL = {
    "Accept": [Restore.ResultCode.RESULT_CODE_SUCCESS],
    "Reject": [Restore.ResultCode.RESULT_CODE_FAILURE,
               Restore.ResultCode.RESULT_CODE_UNKNOWN_SESSION,
               Restore.ResultCode.RESULT_CODE_ACCESS_DENIED,
               Restore.ResultCode.RESULT_CODE_INVALID_PARAMS]
    }


from EC_API.ext.WebAPI.historical_2_pb2 import TimeAndSalesReport as TSR
from EC_API.ext.WebAPI.historical_2_pb2 import BarReportStatusCode as BRS
from EC_API.ext.WebAPI.historical_2_pb2 import VolumeProfileReport as VPR


TIMESALES_REPORT_RESULT_ENUMS_BOOL = {
    "Accept": [TSR.ResultCode.RESULT_CODE_SUCCESS,
              TSR.ResultCode.RESULT_CODE_DROPPED], 
    "Reject": [TSR.ResultCode.RESULT_CODE_DISCONNECTED,
              TSR.ResultCode.RESULT_CODE_FAILURE,
              TSR.ResultCode.RESULT_CODE_ACCESS_DENIED,
              TSR.ResultCode.RESULT_CODE_NOT_FOUND,
              TSR.ResultCode.RESULT_CODE_OUTSIDE_ALLOWED_RANGE,
              TSR.ResultCode.RESULT_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
              TSR.ResultCode.RESULT_CODE_REQUEST_RATE_LIMIT_VIOLATION,
              TSR.ResultCode.RESULT_CODE_NOT_SUPPORTED,
              TSR.ResultCode.RESULT_CODE_INVALID_PARAMS,
              ]
    }

BAR_REPORT_STATUS_ENUMS_BOOL = {
    "Accept": [BRS.BAR_REPORT_STATUS_CODE_SUCCESS,
               BRS.BAR_REPORT_STATUS_CODE_SUBSCRIBED,
               BRS.BAR_REPORT_STATUS_CODE_DROPPED,
               BRS.BAR_REPORT_STATUS_CODE_UPDATE],
    "Reject": [BRS.BAR_REPORT_STATUS_CODE_DISCONNECTED,
               BRS.BAR_REPORT_STATUS_CODE_INVALIDATED,
               BRS.BAR_REPORT_STATUS_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
               BRS.BAR_REPORT_STATUS_CODE_FAILURE,
               BRS.BAR_REPORT_STATUS_CODE_ACCESS_DENIED,
               BRS.BAR_REPORT_STATUS_CODE_NOT_FOUND,
               BRS.BAR_REPORT_STATUS_CODE_OUTSIDE_ALLOWED_RANGE,
               BRS.BAR_REPORT_STATUS_CODE_INVALID_PARAMS,
               BRS.BAR_REPORT_STATUS_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
               BRS.BAR_REPORT_STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION,
               BRS.BAR_REPORT_STATUS_CODE_REQUEST_RATE_LIMIT_VIOLATION,
               BRS.BAR_REPORT_STATUS_CODE_NOT_SUPPORTED,
               BRS.BAR_REPORT_STATUS_CODE_UPDATE_INTERVAL_OUTSIDE_ALLOWED_RANGE
               ]
    }

VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL = {
    "Accept": [VPR.ResultCode.RESULT_CODE_SUCCESS,
               VPR.ResultCode.RESULT_CODE_DROPPED,
               ],
    "Reject": [VPR.ResultCode.RESULT_CODE_DISCONNECTED,
               VPR.ResultCode.RESULT_CODE_FAILURE,
               VPR.ResultCode.RESULT_CODE_ACCESS_DENIED,
               VPR.ResultCode.RESULT_CODE_NOT_FOUND,
               VPR.ResultCode.RESULT_CODE_OUTSIDE_ALLOWED_RANGE,
               VPR.ResultCode.RESULT_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
               VPR.ResultCode.RESULT_CODE_NOT_SUPPORTED,
               VPR.ResultCode.RESULT_CODE_INVALID_PARAMS
               ]
    }

from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MDSS

MARKETDATA_SUB_STATUS_ENUMS_BOOL = {
    "Accept": [MDSS.StatusCode.STATUS_CODE_SUCCESS,
               ],
    "Reject": [MDSS.StatusCode.STATUS_CODE_DISCONNECTED,
               MDSS.StatusCode.STATUS_CODE_FAILURE,
               MDSS.StatusCode.STATUS_CODE_INVALID_PARAMS,
               MDSS.StatusCode.STATUS_CODE_ACCESS_DENIED,
               MDSS.StatusCode.STATUS_CODE_DELETED,
               MDSS.StatusCode.STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION,
               MDSS.StatusCode.STATUS_CODE_CONTRIBUTOR_REQUIRED,
               MDSS.StatusCode.STATUS_CODE_SUBSCRIPTION_RATE_LIMIT_VIOLATION,
               MDSS.StatusCode.STATUS_CODE_NOT_SUPPORTED,
               ]
    }

from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as IR

INFORMATION_REPORT_STATUS_ENUMS_BOOL = {
    "Accept": [IR.StatusCode.STATUS_CODE_SUCCESS,
               IR.StatusCode.STATUS_CODE_SUBSCRIBED,
               IR.StatusCode.STATUS_CODE_DROPPED,
               IR.StatusCode.STATUS_CODE_UPDATE
               ],
    "Reject": [IR.StatusCode.STATUS_CODE_DISCONNECTED,
               IR.StatusCode.STATUS_CODE_FAILURE,
               IR.StatusCode.STATUS_CODE_INVALID_PARAMS,
               IR.StatusCode.STATUS_CODE_NOT_FOUND,
               IR.StatusCode.STATUS_CODE_REQUEST_RATE_LIMIT_VIOLATION,
               IR.StatusCode.STATUS_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
               IR.StatusCode.STATUS_CODE_TOO_LARGE_RESPONSE
               ],
    "Transit": []
    }

from EC_API.ext.common.shared_1_pb2 import OrderStatus as OS
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus as TSS
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus as GFS

TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL = {
    "Accept": [TSS.StatusCode.STATUS_CODE_SUCCESS],
    "Reject": [TSS.StatusCode.STATUS_CODE_DISCONNECTED,
               TSS.StatusCode.STATUS_CODE_FAILURE,
               TSS.StatusCode.STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION,
               TSS.StatusCode.STATUS_CODE_INVALID_PUBLICATION_ID,
               TSS.StatusCode.STATUS_CODE_SUBSCRIBED_ACCOUNTS_LIMIT_VIOLATION
               ],
    }

NEWORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING, 
               OS.Status.FILLED,
               OS.Status.SUSPENDED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]
    }

MODIFYORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.IN_MODIFY,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]
    }

CANCELORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.IN_CANCEL,
               OS.Status.CANCELLED,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]
    }


ACTIVEATORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.ACTIVEAT,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.APPROVE_REJECTED,
               OS.Status.EXPIRED,
               OS.Status.DISCONNECTED], 
    "Transit": [OS.Status.IN_TRANSIT,]
    }

GOFLAT_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [GFS.StatusCode.STATUS_CODE_COMPLETED],
    "Reject": [GFS.StatusCode.STATUS_CODE_TIMED_OUT,
               GFS.StatusCode.STATUS_CODE_FAILED]
    }

ORDER_REJECT_CODE_ENUMS_BOOL = {
    "Accept": [i for i in range(1001, 1257)] + [99]
    }
# Refer back to https://help.cqg.com/apihelp/#!Documents/rejectcodesfixconnectorderrouting.htm

TRANSACTION_STATUS_ENUMS_BOOL = {}

# =============================================================================
# # Define Order statuses
# IN_TRANSIT = OrderStatus.Status.IN_TRANSIT  # Original order is sent to execution system.
# REJECTED = OrderStatus.Status.REJECTED # Order is rejected.
# WORKING = OrderStatus.Status.WORKING # Order is acknowledged by execution system and perhaps partially filled.
# EXPIRED = OrderStatus.Status.EXPIRED # Order is expired.
# IN_CANCEL = OrderStatus.Status.IN_CANCEL #Cancel request is sent to execution system.
# IN_MODIFY = OrderStatus.Status.IN_MODIFY # Modify request is sent to execution system.
# CANCELLED = OrderStatus.Status.CANCELLED # Order is canceled.
# FILLED = OrderStatus.Status.FILLED # Order is completely filled by execution system.
# SUSPENDED = OrderStatus.Status.SUSPENDED # Order is waiting submission to execution system.
# DISCONNECTED = OrderStatus.Status.DISCONNECTED # Order may be canceled because a disconnect occurred.
# ACTIVEAT = OrderStatus.Status.ACTIVEAT # Order will be placed at a specified time (waiting execution system to start accepting orders).
# APPROVE_REQUIRED = OrderStatus.Status.APPROVE_REQUIRED # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
# APPROVED_BY_EXCHANGE = OrderStatus.Status.APPROVED_BY_EXCHANGE
# APPROVE_REJECTED = OrderStatus.Status.APPROVE_REJECTED
# MATCHED = OrderStatus.Status.MATCHED
# PARTIALLY_MATCHED = OrderStatus.Status.PARTIALLY_MATCHED
# TRADE_BROKEN = OrderStatus.Status.TRADE_BROKEN
# =============================================================================

SERVER_MSG_FAMILY = {
    # (1) connection/session
    "logon_result": "session",
    "restore_or_join_session_result": "session",
    "concurrent_connection_join_results": "session",
    "logged_off": "session",
    "pong": "session",
    # (2) info report container
    "information_reports": "info",
    # (3) order/account RPC & streams
    "order_request_rejects": "rpc_reqid",
    "order_request_acks": "rpc_reqid",
    "trade_subscription_statuses": "sub",
    "trade_snapshot_completions": "sub",
    "order_statuses": "substream",
    "position_statuses": "substream",
    "account_summary_statuses": "substream",
    "go_flat_statuses": "rpc_reqid",
    # (4) realtime
    "market_data_subscription_statuses":  "md",
    "real_time_market_data": "md",
    # (5) historical
    "time_and_sales_reports": "rpc_reqid",
    "time_bar_reports": "rpc_reqid",
    "volume_profile_reports": "rpc_reqid",
    "non_timed_bar_reports": "rpc_reqid",
}

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
    'information_requests': ["information_reports",
                             "symbol_resolution_report",
                             "session_information_report",
                             "historical_orders_report",
                             "option_maturity_list_report",
                             "instrument_group_report",
                             "at_the_money_strike_report"
                             ],
    'trade_subscriptions': ["trade_subscription_statuses",
                            "trade_snapshot_completions",],
    'order_requests': [
        "order_statuses", 
        "go_flat_statuses",
        "order_request_rejects",
        "order_request_acks",
        "position_statuses",
        "account_summary_statuses"
        ],
    'market_data_subscriptions': ["market_data_subscription_statuses",
                                  "real_time_market_data"],
    'time_and_sales_requests': ["time_and_sales_reports"],
    'time_bar_requests': ["time_bar_reports"],
    'volume_profile_requests': ["volume_profile_reports"],
    'non_timed_bar_requests': ["non_timed_bar_reports"]
    }


REQUEST_TO_REPLY = {
  "logon": "logon_result",
  "logoff": "logged_off",
  "restore_or_join_session": "restore_or_join_session_result",
  "ping": "pong",
  "pong": "ping",
  #
  "information_requests": "information_reports",
  #
  "trade_subscriptions": "trade_subscription_statuses",
  #
  "order_requests":"order_statuses",
  #
  "market_data_subscriptions": "market_data_subscription_statuses",
  #
  "time_and_sales_requests": "historical_data_reports",
  "time_bar_requests": "time_and_sales_reports",
  "volume_profile_requests": "",
#
  
  "historical_orders_request": "historical_orders_report"
}

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
