#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:43:36 2025

@author: dexter
"""

from datetime import datetime, timezone, timedelta
from EC_API.monitor.cqg.builders import (
    build_realtime_data_request_msg,
    build_reset_tracker_request_msg,
    build_trade_info_request_msg
    )
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as CQG_MDS

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
        contract_id= 102,
        request_id = 222,

        )
    assert msg.market_data_subscriptions[0].contract_id == 102
    assert msg.market_data_subscriptions[0].request_id == 222
    assert msg.market_data_subscriptions[0].level == CQG_MDS.Level.LEVEL_NONE


def test_build_trade_info_request_msg_valid() -> None:
    FROM_DT = datetime.now(timezone.utc) - timedelta(days=10)
    TO_DT = datetime.now(timezone.utc) - timedelta(days=1)
    
    FROM_DT = FROM_DT.timestamp()
    TO_DT = TO_DT.timestamp()
    
    msg = build_trade_info_request_msg(
        account_id = 10001,
        request_id = 333,
        from_date_timestamp = FROM_DT,
        to_date_timestamp = TO_DT,
        )
    assert msg.information_requests[0].id == 333
    assert msg.information_requests[0].historical_orders_request.account_ids[0] == 10001
    assert msg.information_requests[0].historical_orders_request.from_date == int(FROM_DT)
    assert msg.information_requests[0].historical_orders_request.to_date == int(TO_DT)


#_instrument_gp_request
# test_instrument_gp_request_sub
# test_sym_underlying
#test_sym_underlying_sub
#test_atmoney_strike
#test_atmoney_strike_sub

