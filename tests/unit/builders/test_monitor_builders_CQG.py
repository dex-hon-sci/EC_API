#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:43:36 2025

@author: dexter
"""
import pytest
from datetime import datetime, timezone, timedelta
from EC_API.monitor.cqg.builders import (
    build_realtime_data_request_msg,
    build_reset_tracker_request_msg,
    )
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as CQG_MDS
from EC_API.exceptions import MsgBuilderError

def test_build_realtime_data_request_msg_valid() -> None:
    msg = build_realtime_data_request_msg(
        contract_id= 101,
        request_id = 111,
        level = MktDataSubLevelCQG.LEVEL_END_OF_DAY
        )
    assert msg.market_data_subscriptions[0].contract_id == 101
    assert msg.market_data_subscriptions[0].request_id == 111
    assert msg.market_data_subscriptions[0].level == CQG_MDS.Level.LEVEL_END_OF_DAY
    

def test_build_reset_tracker_request_msg_valid() -> None:
    msg = build_reset_tracker_request_msg(
        contract_id = 102,
        request_id = 222,
        )
    assert msg.market_data_subscriptions[0].contract_id == 102
    assert msg.market_data_subscriptions[0].request_id == 222
    assert msg.market_data_subscriptions[0].level == CQG_MDS.Level.LEVEL_NONE


def test_build_realtime_data_request_msg_invalid_inputs() -> None:
    with pytest.raises(MsgBuilderError):
        build_realtime_data_request_msg(
            contract_id= "101", # <--wrong inputs
            request_id = "111", #
            level = MktDataSubLevelCQG.LEVEL_END_OF_DAY
            )
        
def test_build_reset_tracker_request_msg_invalid_inputs() -> None:
    with pytest.raises(MsgBuilderError):
        build_reset_tracker_request_msg(
            contract_id = '102',
            request_id = '222',
            )
        
#_instrument_gp_request
# test_instrument_gp_request_sub
# test_sym_underlying
#test_sym_underlying_sub
#test_atmoney_strike
#test_atmoney_strike_sub

