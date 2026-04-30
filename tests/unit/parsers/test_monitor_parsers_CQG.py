#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:35:02 2026

@author: dexter
"""
import pytest
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MktDSubStatus
from EC_API.ext.WebAPI.market_data_2_pb2 import Quote, TradingState
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enum_mapping import MKTDATASUBLEVEL_MAP_INT2CQG
from EC_API.monitor.cqg.parsers import (
    parse_real_time_market_data,
    parse_market_data_subscription_statuses
    )
from tests.unit.fixtures.server_msg_builders_CQG import (
    build_simple_real_time_market_data_only_1quote_server_msg
    )
from tests.unit.fixtures.server_msg_streams_CQG import (
    build_market_data_subscription_statuses_server_msg,
    build_real_time_market_data_server_msg
    ,
    dummy_realtime_data_stream, 
    dummy_order_update_stream
    )
from EC_API._typing import (
    MarketValueTypeCQG, 
    QuotesValueTypeCQG
    )
from EC_API._typing import (
    MV_CONTRACT_ID,                      # [0]  contract_id                      int
    MV_SCALED_OPEN,                      # [1]  scaled_open_price                int
    MV_SCALED_HIGH,                      # [2]  scaled_high_price                int
    MV_SCALED_LOW,                       # [3]  scaled_low_price                 int
    MV_SCALED_CLOSE,                     # [4]  scaled_close_price               int
    MV_VOL_SIGNIFICAND,                  # [5]  vol_significand                  int
    MV_VOL_EXPONENT,                     # [6]  vol_exponent                     int
    MV_LAST_PRICE_NO_SETTLEMENT,         # [7]  scaled_last_price_no_settlement  int
    MV_SCALE_EX_CLOSE_PRICE,             # [8]  scaled_exchange_close_price      int
    MV_SCALED_YESTERDAY_SETTLEMENT,      # [9]  scaled_yesterday_settlement      int
    MV_SCALED_INDICATIVE_OPEN,          # [10] scaled_indicative_open           int
    MV_OI_SIGNIFICAND,                  # [11] open_interest_significand        int
    MV_OI_EXPONENT,                     # [12] open_interest_exponent           int
    MV_INDICATIVE_OI_VOL_SIGNIFICAND,   # [13] indicative_open_vol_significand  int
    MV_INDICATIVE_OI_VOL_EXPONENT,      # [14] indicative_open_vol_exponent     int
    MV_TICK_VOL,                        # [15] tick_volume                      int
    MV_SCALED_SETTLEMENT,               # [16] scaled_settlement                int
    MV_SCALED_MARKER_PRICE,             # [17] scaled_marker_price              int
    MV_SCALED_LAST_TRADE_PRICE,         # [18] scaled_last_trade_price          int
    MV_SCALED_TRADE_VOL_SIGNIFICAND,    # [19] last_trade_vol_significand       int
    MV_SCALED_TRADE_VOL_EXPONENT,       # [20] last_trade_vol_exponent          int
    MV_LAST_TRADE_UTC_TIMESTAMP,        # [21] last_trade_utc_timestamp         float  (seconds.nanos)
    MV_CLEARED_FIELDS,                  # [22] cleared_fields                   tuple[int, ...]
    MV_TRADE_DATE,                      # [23] trade_date                       int
    MV_SESSION_INDEX,                   # [24] session_index                    int
    MV_MARKET_YIELDS,                   # [25] market_yields                    tuple  (MarketYieldsCQG)
    MV_SCALED_CURRENCY_RATE_PRICE,      # [26] scaled_currency_rate_price       int
    MV_MARKET_STATE,                    # [27] market_state                     tuple  (MarketStateCQG)
    MV_CORRECT_PRICE_SCALE,             # [28] correct_price_scale              float
    MV_IS_SNAPSHOT,                     # [29] is_snapshot                      bool
    )
from EC_API._typing import (
    Q_CONTRACT_ID,                       # [0]  contract_id              int
    Q_TYPE,                              # [1]  type                     int
    Q_UTC_TIME,                          # [2]  quote_utc_time           int   (microseconds since epoch)
    Q_SCALED_PRICE,                      # [3]  scaled_price             int
    Q_SCALED_SOURCE_PRICE,               # [4]  scaled_source_price      int
    Q_PRICE_YIELD,                       # [5]  price_yield              float
    Q_VOL_SIGNIFICAND,                   # [6]  vol_significand          int
    Q_VOL_EXPONENT,                      # [7]  vol_exponent             int
    Q_INDICATORS,                        # [8]  indicators               tuple[int, ...]
    Q_SALES_CONDITION,                   # [9]  sales_condition          int
    Q_TRADE_ATTRS,                      # [10] trade_attributes         tuple (TradeAttrsCQG)
    Q_SCALED_CURRENCY_RATE_PRICE,       # [11] scaled_currency_rate     int
    Q_SCALED_PREMIUM,                   # [12] scaled_premium           int
    Q_MARKET_STATE,                     # [13] market_state             tuple (MarketStateCQG)
    Q_CORRECT_PRICE_SCALE,              # [14] correct_price_scale      float
    Q_IS_SNAPSHOT,                      # [15] is_snapshot              bool
    )
from EC_API._typing import (
    MY_YIELD_OPEN_PRICE,                 # [0]  yield_of_open_price              float
    MY_YIELD_HIGH_PRICE,                 # [1]  yield_of_high_price              float
    MY_YIELD_LOW_PRICE,                  # [2]  yield_of_low_price               float
    MY_YIELD_CLOSE_PRICE,                # [3]  yield_of_close_price             float
    MY_YIELD_YESTERDAY_SETTLEMENT,       # [4]  yield_of_yesterday_settlement    float
    MY_YIELD_INDICATIVE_OPEN,           # [5]  yield_of_indicative_open         float
    MY_YIELD_SETTLEMENT,                # [6]  yield_of_settlement              float
    )
# MarketStateCQG layout (nested in quotes [13] and market_values [27]):
from EC_API._typing import (
    MS_EXCHANGE_STATE,                   # [0]  exchange_state                   int    (PRE_OPEN/OPEN/CLOSED/HALTED/SUSPENDED)
    MS_ALLOW_PLACE_ORDER,                # [1]  allow_place_order                bool
    MS_ALLOW_CANCEL_ORDER,               # [2]  allow_cancel_order               bool
    MS_ALLOW_MODIFY_ORDER,               # [3]  allow_modify_order               bool
    MS_MATCH_ENABLED,                    # [4]  matching_enabled                 bool
    MS_IS_SNAPSHOT                      # [5]  is_snapshot                      bool
    )
# TradeAttrsCQG layout (...)
from EC_API._typing import (
    TA_BUYER,                            # [0]  buyer                    int
    TA_SELLER,                           # [1]  seller                   int
    TA_TRADE_TYPE,                       # [2]  trade_type               str
    TA_MATCH_ID,                         # [3]  match_id                 str
    TA_AGREEMENT_TIME_UTC,               # [4]  agreement_time_utc       float (seconds.nanos)
    )
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
    
    # check RTMD CQG format
    assert isinstance(res,tuple)
    assert len(res) == 4
    
    # --- Check the two quotes ---
    assert len(res[0]) == 2 # two quotes data
    assert len(res[0][0]) ==16  and len(res[0][1]) == 16 # two quotes data
    # --- Quote 0
    assert res[0][0][Q_CONTRACT_ID] == 1 # contract_id
    assert res[0][0][Q_TYPE] == Quote.Type.TYPE_TRADE
    assert res[0][0][Q_SCALED_PRICE] == 19201
    assert res[0][0][Q_SCALED_SOURCE_PRICE] == 10029
    assert res[0][0][Q_PRICE_YIELD] == 100
    assert res[0][0][Q_VOL_SIGNIFICAND] == 0
    assert res[0][0][Q_VOL_EXPONENT] == 2
    assert res[0][0][Q_INDICATORS] == (Quote.Indicator.INDICATOR_OPEN,)
    assert res[0][0][Q_SALES_CONDITION] == Quote.SalesCondition.SALES_CONDITION_HIT
    assert res[0][0][Q_TRADE_ATTRS] == (
        12, 11, "trade_type_1", "match_id_1", 1001 + 5/1e9 
        )
    assert res[0][0][Q_SCALED_CURRENCY_RATE_PRICE] == 32
    assert res[0][0][Q_SCALED_PREMIUM] == 11
    assert res[0][0][Q_MARKET_STATE] == (
        TradingState.ExchangeState.EXCHANGE_STATE_PRE_OPEN, 
        False, True, False, True, True
        )
    assert res[0][0][Q_CORRECT_PRICE_SCALE] == 10.123
    assert res[0][0][Q_IS_SNAPSHOT] == False
    # --- Quote 1
    assert res[0][1][Q_CONTRACT_ID] == 1 # contract_id
    assert res[0][1][Q_TYPE] == Quote.Type.TYPE_TRADE
    assert res[0][1][Q_SCALED_PRICE] == 1400
    assert res[0][1][Q_SCALED_SOURCE_PRICE] == 129
    assert res[0][1][Q_PRICE_YIELD] == 100
    assert res[0][1][Q_VOL_SIGNIFICAND] == 0
    assert res[0][1][Q_VOL_EXPONENT] == 1
    assert res[0][1][Q_INDICATORS] == (Quote.Indicator.INDICATOR_OPEN,)
    assert res[0][1][Q_SALES_CONDITION] == Quote.SalesCondition.SALES_CONDITION_HIT
    
    assert res[0][1][Q_TRADE_ATTRS] == (
        12, 11, "trade_type_2", "match_id_2", 1001 + 5/1e9
        )
    assert res[0][1][Q_SCALED_CURRENCY_RATE_PRICE] == 32
    assert res[0][1][Q_SCALED_PREMIUM] == 11
    assert res[0][1][Q_MARKET_STATE] == (
        TradingState.ExchangeState.EXCHANGE_STATE_PRE_OPEN, 
        False, True, False, True, True
        )
    assert res[0][1][Q_CORRECT_PRICE_SCALE] == 10.123
    assert res[0][1][Q_IS_SNAPSHOT] == False
    
    # --- market values ---
    assert len(res[1]) == 2
    assert len(res[1][0]) == 30 and len(res[1][1]) == 30 # two quotes data
    # --- market value 0
    assert res[1][0][MV_CONTRACT_ID] == 1 # contract_id
    assert res[1][0][MV_SCALED_OPEN] == 19600 # scaled_open_price
    assert res[1][0][MV_SCALED_HIGH] == 20331 # scaled_high_price
    assert res[1][0][MV_SCALED_LOW] == 18890 # scaled_low_price
    assert res[1][0][MV_SCALED_CLOSE] == 19202 # scaled_close_price
    assert res[1][0][MV_VOL_SIGNIFICAND] == 12 #volume_significand
    assert res[1][0][MV_VOL_EXPONENT] == 0  # volume_exponent
    assert res[1][0][MV_LAST_PRICE_NO_SETTLEMENT]  == 266
    assert res[1][0][MV_SCALE_EX_CLOSE_PRICE]  == 277
    assert res[1][0][MV_SCALED_YESTERDAY_SETTLEMENT] == 288
    assert res[1][0][MV_SCALED_INDICATIVE_OPEN] == 8
    assert res[1][0][MV_OI_SIGNIFICAND] == 121
    assert res[1][0][MV_OI_EXPONENT] == 2
    assert res[1][0][MV_INDICATIVE_OI_VOL_SIGNIFICAND] == 1
    assert res[1][0][MV_INDICATIVE_OI_VOL_EXPONENT] == 0
    assert res[1][0][MV_TICK_VOL] == 100
    assert res[1][0][MV_SCALED_SETTLEMENT] == 12411
    assert res[1][0][MV_SCALED_MARKER_PRICE] == 129
    assert res[1][0][MV_SCALED_LAST_TRADE_PRICE] == 18221
    assert res[1][0][MV_SCALED_TRADE_VOL_SIGNIFICAND] == 21
    assert res[1][0][MV_SCALED_TRADE_VOL_EXPONENT] == 5
    assert res[1][0][MV_CLEARED_FIELDS] == (1,)
    assert res[1][0][MV_TRADE_DATE] == 20160616
    assert res[1][0][MV_SESSION_INDEX] ==  4
    assert res[1][0][MV_MARKET_YIELDS] == (1,2,3,4,5,6,7) 
    assert res[1][0][MV_SCALED_CURRENCY_RATE_PRICE] == 10
    assert res[1][0][MV_MARKET_STATE] == (
        TradingState.ExchangeState.EXCHANGE_STATE_PRE_OPEN, 
        False, True, False, True, True
        )
    assert res[1][0][MV_CORRECT_PRICE_SCALE] == 10.123
    assert res[1][0][MV_IS_SNAPSHOT] == False
    # market value 1
    assert res[1][1][MV_CONTRACT_ID] == 1 # contract_id
    assert res[1][1][MV_SCALED_OPEN] == 786 # scaled_open_price
    assert res[1][1][MV_SCALED_HIGH] == 890 # scaled_high_price
    assert res[1][1][MV_SCALED_LOW] == 611 # scaled_low_price
    assert res[1][1][MV_SCALED_CLOSE] == 755 # scaled_close_price
    assert res[1][1][MV_VOL_SIGNIFICAND] == 4 #volume_significand
    assert res[1][1][MV_VOL_EXPONENT] == 0  # volume_exponent
    assert res[1][1][MV_LAST_PRICE_NO_SETTLEMENT] == 266  
    assert res[1][1][MV_SCALE_EX_CLOSE_PRICE] == 277
    assert res[1][1][MV_SCALED_YESTERDAY_SETTLEMENT] == 288 
    assert res[1][1][MV_SCALED_INDICATIVE_OPEN] == 2
    assert res[1][1][MV_OI_SIGNIFICAND] == 1234
    assert res[1][1][MV_OI_EXPONENT] ==  6
    assert res[1][1][MV_INDICATIVE_OI_VOL_SIGNIFICAND] == 5
    assert res[1][1][MV_INDICATIVE_OI_VOL_EXPONENT] == 0
    assert res[1][1][MV_TICK_VOL] == 118
    assert res[1][1][MV_SCALED_SETTLEMENT] == 246
    assert res[1][1][MV_SCALED_MARKER_PRICE] == 803
    assert res[1][1][MV_SCALED_LAST_TRADE_PRICE] == 266
    assert res[1][1][MV_SCALED_TRADE_VOL_SIGNIFICAND] == 21
    assert res[1][1][MV_SCALED_TRADE_VOL_EXPONENT] == 5
    assert res[1][1][MV_CLEARED_FIELDS] == (7,)
    assert res[1][1][MV_TRADE_DATE] == 20170717
    assert res[1][1][MV_SESSION_INDEX] == 4
    assert res[1][1][MV_MARKET_YIELDS] == (
        8, 9, 10, 11, 12, 13, 14
        )
    assert res[1][1][MV_SCALED_CURRENCY_RATE_PRICE] == 26
    assert res[1][1][MV_MARKET_STATE] == (
        TradingState.ExchangeState.EXCHANGE_STATE_PRE_OPEN, 
        False, True, False, True, True
        )
    assert res[1][1][MV_CORRECT_PRICE_SCALE] == 10.123
    assert res[1][1][MV_IS_SNAPSHOT] == False

def test_build_simple_real_time_market_data_only_1quote_valid() -> None:
    server_msg = build_simple_real_time_market_data_only_1quote_server_msg(ServerMsg())
    
    real_time_market_data = server_msg.real_time_market_data
    
    res = parse_real_time_market_data(real_time_market_data[0])

    # --- Check the two quotes ---
    assert len(res[0]) == 1 # one quotes data
    assert len(res[0][0]) ==16 # one quotes data
    # --- Quote 0
    assert res[0][0][Q_CONTRACT_ID] == 1 # contract_id
    assert res[0][0][Q_TYPE] == Quote.Type.TYPE_TRADE
    assert res[0][0][Q_SCALED_PRICE] == 19201
    assert res[0][0][Q_SCALED_SOURCE_PRICE] == 10029
    assert res[0][0][Q_PRICE_YIELD] == 100
    assert res[0][0][Q_VOL_SIGNIFICAND] == 0
    assert res[0][0][Q_VOL_EXPONENT] == 2
    assert res[0][0][Q_INDICATORS] == (Quote.Indicator.INDICATOR_OPEN,)
    assert res[0][0][Q_SALES_CONDITION] == Quote.SalesCondition.SALES_CONDITION_HIT
    assert res[0][0][Q_TRADE_ATTRS] == (
        None, None, None, None, None
        )
    assert res[0][0][Q_SCALED_CURRENCY_RATE_PRICE] == 32
    assert res[0][0][Q_SCALED_PREMIUM] == 11
    assert res[0][0][Q_MARKET_STATE] == (
        None, None, None, None, None, None
        )
    assert res[0][0][Q_CORRECT_PRICE_SCALE] == 0.0
    assert res[0][0][Q_IS_SNAPSHOT] == False    
    
def test_parse_real_time_market_data_invalid() -> None:
      with pytest.raises(MsgParserError):
          parse_real_time_market_data(None)
        