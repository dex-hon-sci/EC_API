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

