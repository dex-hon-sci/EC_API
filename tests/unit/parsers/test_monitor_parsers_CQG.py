#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:35:02 2026

@author: dexter
"""
import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import Quote

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
from EC_API._typing import (MarketValueType, QuotesValueType)
from EC_API.exceptions import MsgParserError


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
   
def test_parse_market_data_subscription_statuses_invalid() -> None:
      with pytest.raises(MsgParserError):
          parse_market_data_subscription_statuses(None)
          
def test_parser_real_data_stream_valid() -> None: 
    server_msg = build_real_time_market_data_server_msg(ServerMsg())
    
    real_time_market_data = server_msg.real_time_market_data
    
    res = parse_real_time_market_data(real_time_market_data[0])
    
    assert isinstance(res,tuple)
    assert len(res) == 3
    
    # quotes
    assert len(res[0]) == 2 # two quotes data
    assert len(res[0][0]) == 8 and len(res[0][1]) == 8 # two quotes data
    
    assert res[0][0][0] == 1 # contract_id
    assert res[0][0][1] == Quote.Type.TYPE_TRADE
    assert res[0][0][3] == 19201
    assert res[0][0][4] == 10029
    assert res[0][0][5] == 0
    assert res[0][0][6] == 2
    assert not res[0][0][7]
    
    assert res[0][1][0] == 1 # contract_id
    assert res[0][1][1] == Quote.Type.TYPE_TRADE # type
    assert res[0][1][3] == 1400 # scaled price
    assert res[0][1][4] == 129 # scaled source price
    assert res[0][1][5] == 0 # volume.significand
    assert res[0][1][6] == 1 # volume.exponent
    assert not res[0][1][7]
    
    # market values
    assert len(res[1]) == 2
    assert len(res[1][0]) == 8 and len(res[1][1]) == 8 # two quotes data

    assert res[1][0][0] == 1 # contract_id
    assert res[1][0][1] == 19600 # scaled_open_price
    assert res[1][0][2] == 20331 # scaled_high_price
    assert res[1][0][3] == 18890 # scaled_low_price
    assert res[1][0][4] == 19202 # scaled_close_price
    assert res[1][0][5] == 12 #volume_significand
    assert res[1][0][6] == 0  # volume_exponent
    assert not res[1][0][7] # correct_price_scale
    # (contract_id, O, H, L, C, volume_significand, volume_exponent, 
    # correct_price_scale)
    assert res[1][1][0] == 1 # contract_id
    assert res[1][1][1] == 786 # scaled_open_price
    assert res[1][1][2] == 890 # scaled_high_price
    assert res[1][1][3] == 611 # scaled_low_price
    assert res[1][1][4] == 755 # scaled_close_price
    assert res[1][1][5] == 16 #volume_significand
    assert res[1][1][6] == 0  # volume_exponent
    assert not res[1][1][7] # correct_price_scale

def test_parse_real_time_market_data_invalid() -> None:
      with pytest.raises(MsgParserError):
          parse_real_time_market_data(None)

# =============================================================================
#
#MarketValueType = tuple[int, int, int, int, int, int, int]#
#
## (contract_id, type, quote_utc_time, scaled_price, scaled_source_price, 
## volume_significand, volume_exponent, scaled_currency_rate_price)
#QuotesValueType = tuple[int, int, Any, int, int, int, int, float]
#         server_msg: ServerMsg,
#         contract_id: int = 1
#     ) -> ServerMsg:

# =============================================================================
#     
#     real_time_market_data = server_msg.real_time_market_data.add()
#     
#     real_time_market_data.contract_id = contract_id
#     
#     # ----
#     quotes = real_time_market_data.quotes.add()
#     quotes.quote_utc_time = int(datetime.now().timestamp())
#     quotes.type = Quote.Type.TYPE_TRADE
#     quotes.scaled_price = 19201
#     quotes.scaled_source_price = 10029
#     quotes.volume.exponent = 2
#     quotes.indicators.append(Quote.Indicator.INDICATOR_OPEN)
#     quotes.sales_condition = Quote.SalesCondition.SALES_CONDITION_HIT
#     
#     # ----
#     market_values = real_time_market_data.market_values.add()
#     
#     market_values.scaled_open_price = 
#     market_values.scaled_high_price = 20331
#     market_values.scaled_low_price = 18890
#     market_values.scaled_close_price = 19202
#     market_values.total_volume.significand = 12
#     
#     # ----
#     quotes1 = real_time_market_data.quotes.add()
#     quotes1.quote_utc_time = int(datetime.now().timestamp())
#     quotes1.type = Quote.Type.TYPE_TRADE
#     quotes1.scaled_price = 1400
#     quotes1.scaled_source_price = 129
#     quotes1.volume.exponent = 1
#     quotes1.indicators.append(Quote.Indicator.INDICATOR_OPEN)
#     quotes1.sales_condition = Quote.SalesCondition.SALES_CONDITION_HIT
#     
#     # ----
#     market_values1 = real_time_market_data.market_values.add()
#     
#     market_values1.scaled_open_price = 786
#     market_values1.scaled_high_price = 890
#     market_values1.scaled_low_price = 611
#     market_values1.scaled_close_price = 755
#     market_values.total_volume.significand = 16
# 
#     return server_msg
# =============================================================================
    