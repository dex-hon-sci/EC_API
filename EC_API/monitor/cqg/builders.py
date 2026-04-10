#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 21:00:05 2025

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.protocol.cqg.builder_util import (
    assert_input_types
    )
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API.monitor.cqg.enum_mapping import MKTDATASUBLEVEL_MAP_INT2CQG
from EC_API.exceptions import MsgBuilderError

REALTIMEDATA_REQUEST_REQUIRED_FIELDS = {
    'contract_id': ('contract_id', int, None),
    'request_id': ('request_id', int, None),
    'level': ('level', MktDataSubLevel|MktDataSubLevelCQG, None)
    }

RESETTRACKER_REQUEST_REQUIRED_FIELDS = {
    'contract_id': ('contract_id', int, None),
    'request_id': ('request_id', int, None),
    }


def build_realtime_data_request_msg(
        contract_id: int, 
        request_id: int, 
        level: MktDataSubLevel | MktDataSubLevelCQG
    ) -> ClientMsg:
    
    params = locals().copy()
    try:
        assert_input_types(params, REALTIMEDATA_REQUEST_REQUIRED_FIELDS)        
    except (KeyError, TypeError, ValueError) as e:
        raise MsgBuilderError(f"build_realtime_data_request_msg invalid parameters: {str(e)}")
        
    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = request_id
    subscription.level = MKTDATASUBLEVEL_MAP_INT2CQG.get(level)
    return client_msg

def build_reset_tracker_request_msg(
        contract_id: int,
        request_id: int
    ) -> ClientMsg:
    
    params = locals().copy()
    try:
        assert_input_types(params, RESETTRACKER_REQUEST_REQUIRED_FIELDS)        
    except (KeyError, TypeError, ValueError) as e:
        raise MsgBuilderError(f"build_realtime_data_request_msg invalid parameters: {str(e)}")

    client_msg = ClientMsg()
    subscription = client_msg.market_data_subscriptions.add()
    subscription.contract_id = contract_id
    subscription.request_id = request_id
    subscription.level = MKTDATASUBLEVEL_MAP_INT2CQG.get(MktDataSubLevel.LEVEL_NONE)
    return client_msg

