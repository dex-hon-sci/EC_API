#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 01:06:27 2026

@author: dexter
"""
from typing import Any, Iterable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import RealTimeMarketData, MarketState
from EC_API.protocol.cqg.parser_util import register_parser
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API._typing import MarketValueTypeCQG, QuotesValueTypeCQG, ParsedRTMDCQG
from EC_API.exceptions import MsgParserError


@register_parser('market_data_subscription_statuses')
def parse_market_data_subscription_statuses(
        server_msg: ServerMsg
    ) -> list[dict[str, str]]:
    try:
        market_data_subscription_statuses = server_msg.market_data_subscription_statuses
        return [{
            'contract_id': msg.contract_id,
            'status_code': msg.status_code,
            'level': msg.level        
            } for msg in market_data_subscription_statuses]
    except Exception:
        raise MsgParserError("Failed to parse market_data_subscription_statuses")

TARGETS = {
    MktDataSubLevel.LEVEL_TRADES: ["quotes", "market_values"],
    MktDataSubLevel.LEVEL_TRADES_BBA: ["quotes", "market_values"],
    MktDataSubLevel.LEVEL_TRADES_BBA_VOLUMES: ["quotes", "market_values"],
    MktDataSubLevel.LEVEL_TRADES_BBA_DOM: ["quotes"],
    MktDataSubLevelCQG.LEVEL_SETTLEMENTS: ["market_values"],
    MktDataSubLevelCQG.LEVEL_TRADES_BBA_DETAILED_DOM: ["quotes", "market_values", "detailed_dom"],
    MktDataSubLevelCQG.LEVEL_END_OF_DAY: ["market_values"]
    }

def _parse_market_state(     
        market_state: MarketState
    ) -> tuple[int,int,int,int, bool, bool]:
    if market_state is None:
        return (None, None, None, None, None)
    ts = market_state.trading_state
    return (
          ts.exchange_state,       # MS_EXCHANGE_STATE
          ts.allow_place_order,    # MS_ALLOW_PLACE
          ts.allow_cancel_order,   # MS_ALLOW_CANCEL
          ts.allow_modify_order,   # MS_ALLOW_MODIFY
          ts.matching_enabled,     # MS_MATCHING_ENABLED
          market_state.is_snapshot
          ) 

def _parse_quotes(
        real_time_market_data: RealTimeMarketData
    ) -> list[QuotesValueTypeCQG]:
    # QuotesValueTypeCQG layout:
    # [0]  contract_id              int
    # [1]  type                     int
    # [2]  quote_utc_time           int   (microseconds since epoch)
    # [3]  scaled_price             int
    # [4]  scaled_source_price      int
    # [5]  price_yield              float
    # [6]  vol_significand          int
    # [7]  vol_exponent             int
    # [8]  indicators               tuple[int, ...]
    # [9]  sales_condition          int
    # [10] trade_attributes         tuple (TradeAttrsCQG)
    # [11] scaled_currency_rate     int
    # [12] scaled_premium           int
    # [13] market_state             tuple (MarketStateCQG)
    # [14] correct_price_scale      float
    # [15] is_snapshot              bool
    
    contract_id: int = real_time_market_data.contract_id
    mkt_state = _parse_market_state(real_time_market_data.market_state)
    
    res = []
    for ele in real_time_market_data.quotes:
        if ele.HasField('trade_attributes'):
            ta = ele.trade_attributes
            ta_buyer          = ta.buyer
            ta_seller         = ta.seller
            ta_trade_type     = ta.trade_type
            ta_match_id       = ta.match_id
            ta_agreement_time_utc = ta.agreement_time_utc.seconds + \
                                    ta.agreement_time_utc.nanos/1e9
        else:
            ta_buyer = ta_seller = ta_trade_type = None
            ta_match_id = ta_agreement_time_utc = None
        
        
        res.append((# Quote tick tuple layout (CQG)
            contract_id, # Q_CONTRACT_ID = 0
            ele.type, # Q_TYPE = 1
            ele.quote_utc_time, # Q_UTC_TIME = 2
            ele.scaled_price, # Q_SCALED_PRICE = 3
            ele.scaled_source_price, #Q_SCALED_SOURCE_PRICE = 4
            ele.price_yield, #Q_PRICE_YIELD = 5
            ele.volume.significand, #Q_VOL_SIGNIFICAND = 6
            ele.volume.exponent, #Q_VOL_EXPONENT = 7
            tuple(ele.indicators), #Q_INDICATORS = 8 #tuple
            ele.sales_condition, #Q_SALES_CONDITION = 9
            (
                ta_buyer,  #Q_TRADE_ATTRS = 10
                ta_seller, 
                ta_trade_type, 
                ta_match_id, 
                ta_agreement_time_utc
             ), 
            ele.scaled_currency_rate_price, #Q_SCALED_CURRENCY_RATE_PRICE = 11
            ele.scaled_premium, #Q_SCALED_PREMIUM = 12
            mkt_state, #Q_MARKET_STATE = 13 #MARKET STATE
            real_time_market_data.correct_price_scale, #Q_CORRECT_PRICE_SCALE = 14
            real_time_market_data.is_snapshot #Q_IS_SNAPSHOT = 15
            ))
    return res

def _parse_market_values(
        real_time_market_data: RealTimeMarketData
    ) -> list[MarketValueTypeCQG]:
      ### MarketValueTypeCQG layout:
      # [0]  contract_id                      int
      # [1]  scaled_open_price                int
      # [2]  scaled_high_price                int
      # [3]  scaled_low_price                 int
      # [4]  scaled_close_price               int
      # [5]  vol_significand                  int
      # [6]  vol_exponent                     int
      # [7]  scaled_last_price_no_settlement  int
      # [8]  scaled_exchange_close_price      int
      # [9]  scaled_yesterday_settlement      int
      # [10] scaled_indicative_open           int
      # [11] open_interest_significand        int
      # [12] open_interest_exponent           int
      # [13] indicative_open_vol_significand  int
      # [14] indicative_open_vol_exponent     int
      # [15] tick_volume                      int
      # [16] scaled_settlement                int
      # [17] scaled_marker_price              int
      # [18] scaled_last_trade_price          int
      # [19] last_trade_vol_significand       int
      # [20] last_trade_vol_exponent          int
      # [21] last_trade_utc_timestamp         float  (seconds.nanos)
      # [22] cleared_fields                   tuple[int, ...]
      # [23] trade_date                       int
      # [24] session_index                    int
      # [25] market_yields                    tuple  (MarketYieldsCQG)
      # [26] scaled_currency_rate_price       int
      # [27] market_state                     tuple  (MarketStateCQG)
      # [28] correct_price_scale              float
      # [29] is_snapshot                      bool
    res = []
    contract_id = real_time_market_data.contract_id
    mkt_state = _parse_market_state(real_time_market_data.market_state)

    for ele in real_time_market_data.market_values:
        my = ele.market_yields
        
        last_trade_utc_timestamp = ele.last_trade_utc_timestamp.seconds + \
                                   ele.last_trade_utc_timestamp.nanos/1e9
        
        res.append((# MarketValues tick tuple layout (CQG)
            contract_id, #MV_CONTRACT_ID = 0
            ele.scaled_open_price, #MV_SCALED_OPEN = 1
            ele.scaled_high_price, #MV_SCALED_HIGH = 2
            ele.scaled_low_price, #MV_SCALED_LOW = 3
            ele.scaled_close_price, #MV_SCALED_CLOSE = 4
            ele.total_volume.significand, #MV_VOL_SIGNIFICAND = 5
            ele.total_volume.exponent, #MV_VOL_EXPONENT = 6
            ele.scaled_last_price_no_settlement, #MV_LAST_PRICE_NO_SETTLEMENT = 7
            ele.scaled_exchange_close_price, #MV_SCALE_EX_CLOSE_PRICE = 8
            ele.scaled_yesterday_settlement, #MV_SCALED_YESTERDAY_SETTLEMENT = 9
            ele.scaled_indicative_open, #MV_SCALED_INDICATIVE_OPEN = 10
            ele.open_interest.significand, #MV_OI_SIGNIFICAND = 11
            ele.open_interest.exponent, #MV_OI_EXPONENT = 12
            ele.indicative_open_volume.significand, #MV_INDICATIVE_OI_VOL_SIGNIFICAND = 13
            ele.indicative_open_volume.exponent, #MV_INDICATIVE_OI_VOL_EXPONENT = 14
            ele.tick_volume, #MV_TICK_VOL = 15
            ele.scaled_settlement, #MV_SCALED_SETTLEMENT = 16
            ele.scaled_marker_price, #M V_SCALED_MARKER_PRICE = 17 PTMM (Pre-Trade Mid-Market Mark)
            ele.scaled_last_trade_price, #MV_SCALED_LAST_TRADE_PRICE = 18
            ele.last_trade_volume.significand,#MV_SCALED_TRADE_VOL_SIGNIFICAND = 19 
            ele.last_trade_volume.exponent,#MV_SCALED_TRADE_VOL_EXPONENT = 20
            last_trade_utc_timestamp, #MV_LAST_TRADE_UTC_TIMESTAMP = 21 # timestamp
            tuple(ele.cleared_fields),#MV_CLEARED_FIELDS = 22 # tuple
            ele.trade_date, #MV_TRADE_DATE = 23
            ele.session_index, #MV_SESSION_INDEX = 24
            (
                my.yield_of_open_price, #MV_MARKET_YIELDS = 25
                my.yield_of_high_price,
                my.yield_of_low_price,
                my.yield_of_close_price,
                my.yield_of_yesterday_settlement,
                my.yield_of_indicative_open,
                my.yield_of_settlement
             ),               
            ele.scaled_currency_rate_price, #MV_SCALED_CURRENCY_RATE_PRICE = 26
            mkt_state, #MV_MARKET_STATE = 27 #MARKET STATE
            real_time_market_data.correct_price_scale, #MV_CORRECT_PRICE_SCALE = 28
            real_time_market_data.is_snapshot #MV_IS_SNAPSHOT = 29
            ))
    return res

def _parse_detailed_DOMs(): return



@register_parser('real_time_market_data')
def parse_real_time_market_data(
        real_time_market_data: RealTimeMarketData, 
    ) -> ParsedRTMDCQG:
    try:
        # Master function that handle real time market data by provided levels
        quotes = _parse_quotes(real_time_market_data) if real_time_market_data.quotes else []
        mkt_vals = _parse_market_values(real_time_market_data) if real_time_market_data.market_values else []
        dtl_DOMs = [] # fix later
        corrections = _parse_quotes(real_time_market_data) if real_time_market_data.corrections else []
        return quotes, mkt_vals, dtl_DOMs, corrections
    except  Exception:
        raise MsgParserError("Failed to parse real_time_market_data")
