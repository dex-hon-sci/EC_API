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
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LgRes
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as RstJoinSessRes
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LgOff
from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as InfoRp
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus as TrdSubStatus
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus as GFltStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as MktDSub
from EC_API.ext.WebAPI.historical_2_pb2 import TimeAndSalesReport as TSrRep
from EC_API.ext.WebAPI.historical_2_pb2 import BarReportStatusCode as BarRpStatusCode
from EC_API.ext.WebAPI.historical_2_pb2 import VolumeProfileReport as VolPrfRep

from server_msg_builders_CQG import *
# Unit test for getting the right message type and id
# Unit test for matching request-response
# Unit Test for routing, see if messages are pop and resolve in fut 
 
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
####
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
# build_order_statuses_server_msg # <-- complex
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
    
server_msg1 = build_logon_result_server_msg(LgRes.ResultCode.RESULT_CODE_SUCCESS)
server_msg2 = build_restore_or_join_session_result_server_msg(RstJoinSessRes.ResultCode.RESULT_CODE_SUCCESS)
server_msg3 = build_concurrent_connection_join_results_server_msg(True)
server_msg4 = build_logged_off_server_msg(LgOff.LogoffReason.LOGOFF_REASON_BY_REQUEST)
server_msg5 = build_pong_server_msg(ping_time = int(datetime.now().timestamp()), delay = 5)

server_msg6 = build_symbol_resolution_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)
server_msg7 = build_session_info_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)
server_msg8 = build_historical_orders_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)
server_msg9 = build_option_maturity_list_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)
server_msg10 = build_instrument_group_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)
server_msg11 = build_at_the_money_strike_report_server_msg(InfoRp.StatusCode.STATUS_CODE_SUCCESS)

server_msg12 = build_order_request_rejects_server_msg()
server_msg13 = build_order_request_acks_server_msg()
server_msg14 = build_trade_subscription_statuses_server_msg(TrdSubStatus.StatusCode.STATUS_CODE_SUCCESS)
server_msg15 = build_trade_snapshot_completetions_server_msg()
server_msg16 = build_order_statuses_server_msg(OrderStatus.Status.IN_TRANSIT)
server_msg17 = build_position_statuses_server_msg()
server_msg18 = build_go_flat_statuses_server_msg(GFltStatus.StatusCode.STATUS_CODE_COMPLETED)

server_msg19 = build_market_data_subscription_statuses_server_msg(MktDSubStatus.StatusCode.STATUS_CODE_SUCCESS)
server_msg20 = build_real_time_market_data_server_msg()

server_msg21 = build_time_and_sales_reports_server_msg(TSrRep.ResultCode.RESULT_CODE_SUCCESS)
server_msg22 = build_time_bar_reports_server_msg(BarRpStatusCode.BAR_REPORT_STATUS_CODE_SUCCESS)
server_msg23 = build_volume_profile_reports_server_msg(VolPrfRep.ResultCode.RESULT_CODE_SUCCESS)
server_msg24 = build_non_timed_bar_reports_server_msg(BarRpStatusCode.BAR_REPORT_STATUS_CODE_SUCCESS)

# =============================================================================
# print(server_msg1)
# print(server_msg2)
# print(server_msg3)
# print(server_msg4)
# print(server_msg5)
# 
# print(server_msg6)
# print(server_msg7)
# print(server_msg8)
# print(server_msg9)
# print(server_msg10)
# print(server_msg11)
# 
# print(server_msg12)
# print(server_msg13)
# print(server_msg14)
# print(server_msg15)
# print(server_msg16)
# print(server_msg17)
# print(server_msg18)
# print(server_msg19)
# print(server_msg20)
# print(server_msg21)
# print(server_msg22)
# print(server_msg23)
# print(server_msg24)
# =============================================================================
