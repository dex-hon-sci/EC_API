#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:00:05 2025

@author: dexter
"""
from datetime import datetime
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API.monitor.cqg.enum_mapping import MKTDATASUBLEVEL_MAP_INT2CQG

def build_realtime_data_request_msg(
    contract_id: int, 
    request_id: int, 
    level: MktDataSubLevel | MktDataSubLevelCQG
    ) -> ClientMsg:
    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = request_id # Everytime this is called, it increase by 1
    subscription.level = MKTDATASUBLEVEL_MAP_INT2CQG.get(level)
    return client_msg

def build_reset_tracker_request_msg(
    contract_id: int,
    request_id: int
    ) -> ClientMsg:
    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = request_id
    subscription.level = MKTDATASUBLEVEL_MAP_INT2CQG.get(MktDataSubLevel.LEVEL_NONE)
    return client_msg

def build_trade_info_request_msg(
    account_id: int,
    request_id: int,
    from_date_timestamp: datetime,
    to_date_timestamp: datetime,
    ) -> ClientMsg:
    client_msg = ClientMsg()
    information_requests = client_msg.information_requests.add()
    
    information_requests.id = request_id
    information_requests.historical_orders_request.from_date= int(from_date_timestamp)
    information_requests.historical_orders_request.to_date= int(to_date_timestamp)
    information_requests.historical_orders_request.account_ids.append(account_id)

    return client_msg
# =============================================================================
# 
# def request_historical_orders(client, msg_id, account_id, 
#                               from_date:datetime.datetime, 
#                               to_date:datetime.datetime):
#     
#     from_date_timestamp = from_date.timestamp()
#     to_date_timestamp = to_date.timestamp()
#     
#     client_msg = ClientMsg()
# 
#     information_request = client_msg.information_requests.add()
#     
#     information_request.id = msg_id
#     information_request.historical_orders_request.from_date= int(from_date_timestamp)
#     information_request.historical_orders_request.to_date= int(to_date_timestamp)
#     information_request.historical_orders_request.account_ids.append(account_id)
#         
#     client.send_client_message(client_msg)
# =============================================================================
