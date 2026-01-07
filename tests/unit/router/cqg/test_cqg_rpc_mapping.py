#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  8 06:37:35 2026

@author: dexter
"""
from datetime import datetime, timedelta, timezone
#from EC_API.protocol.cqg.routing import server_msg_type
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.common.shared_1_pb2 import OrderStatus

def build_server_msg_historical_orders_report():
    
    TS = datetime.now(timezone.utc)
    server_msg = ServerMsg()
    
    inportmation_report = server_msg.information_reports.add()
    inportmation_report.id = 1
    
    historical_orders_report_order_status = inportmation_report.historical_orders_report.order_statuses.add()
    historical_orders_report_order_status.status = OrderStatus.Status.FILLED
    historical_orders_report_order_status.order_id = "1"
    historical_orders_report_order_status.chain_order_id = "A"
    historical_orders_report_order_status.status_utc_timestamp = TS
    historical_orders_report_order_status.fill_cnt = 1
    
    print(server_msg)
    return server_msg
    
def server_msg_type(msg: ServerMsg) -> str:
    all_field_names = msg.ListFields()
    print(all_field_names)
    #return msg.WhichOneof("information_reports")  # CQG oneof "message"

    
server_msg = build_server_msg_historical_orders_report()

server_msg_type(server_msg)