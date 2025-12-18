#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:00:05 2025

@author: dexter
"""
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
    msg_id: int,
    ) -> ClientMsg:
    client_msg = ClientMsg()

    return client_msg

