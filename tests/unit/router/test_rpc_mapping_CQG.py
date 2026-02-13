#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 06:37:35 2026

@author: dexter
"""
from datetime import datetime, timedelta, timezone
#from EC_API.protocol.cqg.routing import server_msg_type
from google.protobuf.descriptor import Descriptor, FieldDescriptor
from tests.unit.fixtures.server_msg_builders_CQG import *
# Unit test for getting the right message type and id
# Unit test for matching request-response
# Unit Test for routing, see if messages are pop and resolve in fut 
 
def server_msg_type(msg: ServerMsg) -> str:
    
    print(msg.DESCRIPTOR, msg.DESCRIPTOR.name, msg.DESCRIPTOR.full_name,
          type(msg.DESCRIPTOR.name), type(msg.DESCRIPTOR.full_name))
    print('fields', msg.DESCRIPTOR.fields)
          #'fields_by_number', msg.DESCRIPTOR.fields_by_number, 
          #'fields_by_name', msg.DESCRIPTOR.fields_by_name)
    all_field_names = msg.ListFields()
    print(all_field_names,len(all_field_names))

    for top_fd, top_val in all_field_names:
        print(f'---------{top_fd}')
        print("1-1", top_val.DESCRIPTOR.name)
        
        print("2",top_fd.type, top_val, top_val.HasField('result_code'))
        print(type(top_val))
        print("fd.type_msg", FieldDescriptor.TYPE_MESSAGE)
        print("type_msg", FieldDescriptor.LABEL_REPEATED)
        print("equal", top_fd.type == FieldDescriptor.TYPE_MESSAGE)
        print("equal", top_fd.type == FieldDescriptor.LABEL_REPEATED)

# =============================================================================
#     for fd, val in msg.ListFields():
#         name = fd.name
#         typ = fd.type
#         c_typ = fd.containing_type
#         #field = fd.nested_types
#         print('name', name, typ, c_typ)
#         print('name2', val, type(val[0]))
#         print(val[0].HasField("historical_orders_report"))
# =============================================================================
        
        # cases different message type different treatment
        # 
        # Repeat
                
    #return server_msg_type(msg.)
# =============================================================================
# # id
# #    information_report.id = 1
# #    instruments.id = "id_1"
# 
# build_symbol_resolution_report_server_msg
# build_session_info_report_server_msg
# build_historical_orders_report_server_msg
# build_option_maturity_list_report_server_msg
# build_instrument_group_report_server_msg
# build_at_the_money_strike_report_server_msg
# ###
# ###contract_metadata.contract_id
# ####transaction_statuses.trans_id = 2
# ###trade_snapshot_completions.subscription_id = 1
# build_order_request_rejects_server_msg # request_id
# build_order_request_acks_server_msg # request_id
# build_trade_subscription_statuses_server_msg # id
# build_trade_snapshot_completetions_server_msg ##subscription_id
# build_order_statuses_server_msg # <-- very complex
# build_position_statuses_server_msg # open_positions.id
# build_account_summary_statuses_server_msg
# build_go_flat_statuses_server_msg # request_id
# # contract id
# build_market_data_subscription_statuses_server_msg
# build_real_time_market_data_server_msg
# # Request ID
# build_time_and_sales_reports_server_msg
# build_time_bar_reports_server_msg
# build_volume_profile_reports_server_msg
# build_non_timed_bar_reports_server_msg
# =============================================================================
def extract_conn_key() -> None:...
def extract_info_report_key() -> None:...
def extract_order_status_key() -> None:...
def extract_position_status_key() -> None:...
def extract_go_flat_status_key() -> None:...
def extract_historical_data_keys() -> None:...
    

def test_server_msg_type() -> None:
    
    
    pass
    

