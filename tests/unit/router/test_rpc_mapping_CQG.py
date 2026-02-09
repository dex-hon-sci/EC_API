#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 06:37:35 2026

@author: dexter
"""
from datetime import datetime, timedelta, timezone
#from EC_API.protocol.cqg.routing import server_msg_type
from google.protobuf import descriptor
from google.protobuf.descriptor import FieldDescriptor

from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus

from server_msg_builders_CQG import *
# Unit test for getting the right message type and id
# Unit test for matching request-response
# Unit Test for routing, see if messages are pop and resolve in fut 
# 


### Connection
# logon_result
# restore_or_join_session_result
# logged_off
# pong

### information_report
# accounts_report
# symbol_resolution_report (v)
# session_information_report (v)
# historical_orders_request (v)
# option_maturity_list_report
# instrument_group_report
# at_the_money_strike_report

### Orders
# order_request_rejects
# order_request_acks
# trade_subscription_statuses
# trade_snapshot_completions
# order_statuses
# position_statuses
# account_summary_statuses
# go_flat_statuses

### Data
# market_data_subscription_statuses
# real_time_market_data

## Historical Data
# time_and_sales_reports
# time_bar_reports
# volume_profile_reports
# non_timed_bar_reports


    
def server_msg_type(msg: ServerMsg) -> str:
    all_field_names = msg.ListFields()
    print(len(all_field_names))

    for top_fd, top_val in all_field_names:
        print(top_fd.type, top_val, type(top_val))
        print("fd.type_msg", FieldDescriptor.TYPE_MESSAGE)
        print("type_msg", FieldDescriptor.LABEL_REPEATED)
        print("equal", top_fd.type == FieldDescriptor.TYPE_MESSAGE)
        print("equal", top_fd.type == FieldDescriptor.LABEL_REPEATED)

    for fd, val in msg.ListFields():
        name = fd.name
        typ = fd.type
        c_typ = fd.containing_type
        #field = fd.nested_types
        print('name', name, typ, c_typ)
        print('name2', val, type(val[0]))
        print(val[0].HasField("historical_orders_report"))
        
        # cases different message type different treatment
        # 
        # Repeat
    print(FieldDescriptor.TYPE_MESSAGE)
        
        
    #return server_msg_type(msg.)
    #print(all_field_names[0][1].message_type, 
    #      type(all_field_names[0][1][0]), 
    #      len(all_field_names[0][1]))
    
   # print(msg.HasField("information_reports"))
   # print()
    #return all_field_names[0][1]
    #return msg.WhichOneof("information_reports")  # CQG oneof "message"

    
server_msg = build_logon_result_server_msg()

#server_msg_type(server_msg)

server_msg = build_logon_result_server_msg()
print(server_msg)