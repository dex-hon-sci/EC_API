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

# Unit test for getting the right message type and id
# Unit test for matching request-response
# Unit Test for routing, see if messages are pop and resolve in fut 
# 


def build_information_reports_server_msg():
    pass


def build_():...
    

def build_logon_result_server_msg():...

def build_restore_or_join_session_result_server_msg():...

def build_logged_off_server_msg():...

def build_pong_server_msg():...


def build_order_request_rejects_server_msg():...

def build_order_request_acks_server_msg():...

def build_trade_subscription_statuses_server_msg():...

def build_order_statuses_server_msg():...

def build_position_statuses_server_msg():...

def build_account_summary_statuses_server_msg():...

def build_go_flat_statuses_server_msg():...

def build_market_data_subscription_statuses_server_msg():...

def build_real_time_market_data_server_msg():...


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

    return 

    
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

    
server_msg = build_historical_orders_report_server_msg()

server_msg_type(server_msg)

server_msg = build_symbol_resolution_report_server_msg()
print(server_msg)