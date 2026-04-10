#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:35:02 2026

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus

from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enum_mapping import MKTDATASUBLEVEL_MAP_INT2CQG
from EC_API.monitor.cqg.parsers import (
    parse_real_time_market_data,
    parse_market_data_subscription_statuses
    )

from tests.unit.fixtures.server_msg_streams_CQG import (
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg,
    dummy_realtime_data_stream, 
    dummy_order_update_stream
    )
from EC_API._typing import MarketValueType, QuotesValueType


def test_parse_market_data_subscription_statuses_valid() -> None:
    server_msg = build_market_data_subscription_statuses_server_msg(ServerMsg(),contract_id=3)
    res = parse_market_data_subscription_statuses(server_msg)
    
    assert isinstance(res, list)
    assert len(res) == 1
    for ele in res:
        assert isinstance(ele, dict)
        assert ele['contract_id'] == 3
        assert ele['status_code'] == MktDSubStatus.StatusCode.STATUS_CODE_SUCCESS
        assert ele['level'] == MKTDATASUBLEVEL_MAP_INT2CQG[MktDataSubLevel.LEVEL_TRADES]
   
def test_parse_market_data_subscription_statuses_invalid() -> None:...

# =============================================================================
# def test_parser_real_data_stream_valid() -> None:
#     server_msg = build_real_time_market_data_server_msg()
#     res = parse_real_time_market_data(server_msg)
#     
#     print(res)
#     
#     assert isinstance(res, list)
#     assert len(res) == 2
#     for ele in res:
#         assert isinstance(ele,tuple)
#     
# =============================================================================
    
    
    