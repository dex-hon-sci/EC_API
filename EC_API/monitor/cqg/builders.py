#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:00:05 2025

@author: dexter
"""
from datetime import datetime
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg


def build_realtime_data_request_msg(
    contract_id: int, 
    msg_id: int, 
    level: int
    ) -> ClientMsg:
    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = msg_id # Everytime this is called, it increase by 1
    subscription.level = level

    return client_msg

def build_reset_tracker_request_msg(
    msg_id: int,
    contract_id: int
    ) -> ClientMsg:
    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = msg_id
    subscription.level = 0
    return client_msg

def build_trade_info_request_msg(
    account_id: int,
    msg_id: int,
    from_date_timestamp: datetime,
    to_date_timestamp: datetime,
    ) -> ClientMsg:
    client_msg = ClientMsg()
    information_request = client_msg.information_requests.add()
    
    information_request.id = msg_id
    information_request.historical_orders_request.from_date= int(from_date_timestamp)
    information_request.historical_orders_request.to_date= int(to_date_timestamp)
    information_request.historical_orders_request.account_ids.append(account_id)

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
