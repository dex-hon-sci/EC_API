#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 01:06:27 2026

@author: dexter
"""
from typing import Any, Iterable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.ext.WebAPI.market_data_2_pb2 import RealTimeMarketData
from EC_API.protocol.cqg.parser_util import register_parser
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API._typing import MarketValueType, QuotesValueType, ParsedRTMD
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

def _parse_quotes(
        real_time_market_data: RealTimeMarketData
    ) -> list[QuotesValueType]:
    res = []
    contract_id = real_time_market_data.contract_id

    for ele in real_time_market_data.quotes:
        res.append((
            contract_id,
            ele.type,
            ele.quote_utc_time,
            ele.scaled_price,
            ele.scaled_source_price,
            ele.volume.significand,
            ele.volume.exponent,
            #list(ele.indicators),
            ele.scaled_currency_rate_price
            ))
    return res

def _parse_market_values(
        real_time_market_data: RealTimeMarketData
    ) -> list[MarketValueType]:
    res = []
    contract_id = real_time_market_data.contract_id
    correct_price_scale = real_time_market_data.correct_price_scale

    for ele in real_time_market_data.market_values:
        res.append((
            contract_id,
            ele.scaled_open_price,
            ele.scaled_high_price,
            ele.scaled_low_price,
            ele.scaled_close_price,
            ele.total_volume.significand,
            ele.total_volume.exponent,
            correct_price_scale
            ))
    return res

def _parse_detailed_DOMs(): return

@register_parser('real_time_market_data')
def parse_real_time_market_data(
        real_time_market_data: RealTimeMarketData, 
    ) -> ParsedRTMD:
    # Master function that handle real time market data by provided levels
    quotes = _parse_quotes(real_time_market_data) if real_time_market_data.quotes else []
    mkt_vals = _parse_market_values(real_time_market_data) if real_time_market_data.market_values else []
    dtl_DOMs = [] # fix later
    return quotes, mkt_vals, dtl_DOMs
