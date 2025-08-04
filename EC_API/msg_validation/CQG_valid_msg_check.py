#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 09:28:22 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.base import ValidMsgCheck, MsgCheckPara, MsgCheckPara
from EC_API.msg_validation.CQG_connect_enums import (
    LOGON_RESULT_STATUS_ENUMS_BOOL,
    LOGGEDOFF_REASON_ENUMS_BOOL,
    RESTORE_STATUS_ENUMS_BOOL,
    )
from EC_API.msg_validation.CQG_meta_enums import INFORMATION_REPORT_STATUS_ENUMS_BOOL
from EC_API.msg_validation.CQG_trade_enums import (
    TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL,
    GOFLAT_ORDERSTATUS_ENUMS_BOOL)
from EC_API.msg_validation.CQG_historical_enums import (
    TIMESALES_REPORT_RESULT_ENUMS_BOOL,
    VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL
    )
from EC_API.msg_validation.CQG_market_data_enums import MARKETDATA_SUB_STATUS_ENUMS_BOOL

from google.protobuf.descriptor import FieldDescriptor

# Some msg require a status check and some don't

map_status_enums = {"logon_result": LOGON_RESULT_STATUS_ENUMS_BOOL,
                    "logged_off": LOGGEDOFF_REASON_ENUMS_BOOL,
                    "restore_or_join_session_result": RESTORE_STATUS_ENUMS_BOOL,
                    "information_reprort": INFORMATION_REPORT_STATUS_ENUMS_BOOL,
                    "trade_subscription_statuses": TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL,
                    "order_statuses": {"Accept":[], "Reject":[]},
                    "go_flat_statuses": GOFLAT_ORDERSTATUS_ENUMS_BOOL,
                    "time_and_sales_reports": TIMESALES_REPORT_RESULT_ENUMS_BOOL,
                    "volume_profile_reports": VOLUMEPROFILE_REPORT_RESULT_ENUMS_BOOL,
                    "market_data_subscription_statuses": MARKETDATA_SUB_STATUS_ENUMS_BOOL,
                    }

#order_request_rejects
#order_request_acks
#trade_snapshot_completions
#position_statuses
#collateral_statuses
#account_summary_statuses

#real_time_market_data

#time_bar_reports
#volume_profile_reports
#non_timed_bar_reports


def get_CQG_servermsg_type(server_msg: ServerMsg) -> tuple[list[str]|list[ServerMsg]]:
    found_message_types = []
    found_message_values = []

    for field_descriptor, value in server_msg.ListFields():
        field_name = field_descriptor.name
    
        # For repeated fields, the value is a list. We check if the list
        # is not empty. ListFields() will only return the field if the
        # list has at least one element.
        if field_descriptor.label == FieldDescriptor.LABEL_REPEATED:
            if len(value) > 0:
                found_message_types.append(field_name)
                found_message_values.append(value)
        
        # For optional fields, ListFields() only returns the field
        # if it has been explicitly set.
        else:
            found_message_types.append(field_name)
            found_message_values.append(value)

    return (found_message_types, found_message_values)


class CQGValidMsgCheck(ValidMsgCheck, MsgCheckPara):
    # This class is in charge of validating serverresponse message 
    # AFTER sending a request is sent. 
    # It contains a set of checks that is required to resolve if 
    # we receive the correct set of responses from the server.
    
    # Check message types, map them to their corresponding set of enums
    # Check existence, 
    
    # then check msg types (existence)
    # match requestID first
    # Check specific markers (e.g., is_snapshot)
    # check desired response (matching requestID, orderID, clorderid)

    def __init__(self, server_msg: ServerMsg):
        
        self.msg_types, self.msg_values = get_CQG_servermsg_type(server_msg)
        
    def status_check(self, server_msg: ServerMsg):   
        # match hash table for correct enums, 
        if True:
            self.recv_status = True
            return server_msg
        
    def accept_status_check(self, server_msg: ServerMsg):
        
        for msg_type, msg_value in zip(self.msg_types, self.msg_values):
        # Find out the msg_type
            if msg_value.result_code in map_enums[msg_type]["accept"]:
                self.recv_success_status = True
                return self.server_msg
            
    def reject_status_check(self):
        pass


    def result_check(self, server_msg: ServerMsg):
        if server_msg.result_code == 1:
            self.recv_success_status = True
            return server_msg


# LogonResults Enum
# RestoreOrJoinSessionResult Enum
# LoggedOff Enum

# Information report Enums is_report_complete
# OrderStatus Enum
# TransactionStatus Enum

# OrderRequestReject Enum, OrderRequestAck
# OrderStatus Enum, match OrderID, clorderid

# TradeSubscriptionStatus Enum
# TradeSnapshotCompletion
# PositionStatus, CollateralStatus, AccountSummaryStatus, 
# GoFlatStatus Enum
# MarketDataSubscriptionStatus Enum
# RealTimeMarketData special states
# TimeAndSalesReport Enums
# TimeBarReport state
# VolumeProfileReport Enum


#from google.protobuf import json_format
#json_string = json_format.MessageToJson(server_msg, indent=2)
#print(json_string)
