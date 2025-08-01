#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 09:28:22 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.msg_validation.base import ValidMsgCheck, MsgCheckPara, MsgCheckPara
from google.protobuf.descriptor import FieldDescriptor


map_enums = {"information_reprort": {"Accept":[], "Reject":[]},
             "logon_result": {"Accept":[], "Reject":[]},
             "logged_off": {"Accept":[], "Reject":[]},
             "restore_or_join_session_result": {"Accept":[], "Reject":[]},
             "concurrent_connection_join_results": {"Accept":[], "Reject":[]},
             "order_request_reject": {"Accept":[], "Reject":[]},
             "trade_subscription_statuses": {"Accept":[], "Reject":[]},
             "time_and_sales_reports": {"Accept":[], "Reject":[]},
             "volume_profile_reports": {"Accept":[], "Reject":[]},
             "market_data_subscription_statuses": {"Accept":[], "Reject":[]},
             "order_statuses": {"Accept":[], "Reject":[]},
             "go_flat_statuses": {"Accept":[], "Reject":[]}
             }


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
    
    # check types (existence)
    # Check specific marker
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


# Information report Enums is_report_complete
# OrderStatus Enum
# TransactionStatus Enum
# LogonResults Enum
# RestoreOrJoinSessionResult Enum
# LoggedOff Enum
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
