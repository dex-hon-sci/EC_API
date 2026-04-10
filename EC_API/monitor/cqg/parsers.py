#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 01:06:27 2026

@author: dexter
"""
from typing import Any, Iterable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.key_extractors import walk_fields
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API._typing import MarketValueType, QuotesValueType
from EC_API.exceptions import MsgParserError


TARGET = {
    MktDataSubLevel.LEVEL_TRADES: "quotes",
    MktDataSubLevel.LEVEL_TRADES_BBA: "",
    MktDataSubLevel.LEVEL_TRADES_BBA_VOLUMES: "market_values",
    MktDataSubLevel.LEVEL_TRADES_BBA_DOM: "",
    MktDataSubLevelCQG.LEVEL_SETTLEMENTS: "market_values",
    MktDataSubLevelCQG.LEVEL_TRADES_BBA_DETAILED_DOM: "",
    MktDataSubLevelCQG.LEVEL_END_OF_DAY: ""
    }

def parse_market_data_subscription_statuses(
        server_msg: ServerMsg
        ) -> list[dict[str, str]]:
    market_data_subscription_statuses = server_msg.market_data_subscription_statuses
    
    if not market_data_subscription_statuses:
        raise MsgParserError("Empty field for market_data_subscription_statuses")
    
    return [{
        'contract_id': msg.contract_id,
        'status_code': msg.status_code,
        'level': msg.level        
        } for msg in market_data_subscription_statuses]
        

def parse_real_time_market_data(
        server_msg: ServerMsg, 
        level: MktDataSubLevel | MktDataSubLevelCQG
        ) -> list[MarketValueType]:
    # Master function that handle real time market data by provided levels
    def selector(fd, val) -> Iterable[Any]:
        if fd.message_type is not None and fd.name == "real_time_market_data":
            yield 
        else:
            yield
        
    outs = walk_fields(server_msg, selector, max_depth=1)

    return outs

##def parse_order_statuses_data(server_msg: ServerMsg)-> dict[str,Any]:
#    return 

# =============================================================================
# def parse_real_time_market_data2(server_msg: ServerMsg)-> list[dict[str,Any]]:
#     # Need to walk through the message
#     res = []
#     if server_msg.real_time_market_data:
#         real_time_market_data = server_msg.real_time_market_data
#         price_scale = real_time_market_data.price_scale
#         for data in real_time_market_data:
#             if real_time_market_data:
#                 for ele in data.market_values:
#                     if not ele.total_volume.exponent:
#                         total_vol_exponent = 0
#                     else: 
#                         total_vol_exponent = ele.total_volume.exponent
#                         
#                     if not ele.total_volume.significand:
#                         total_vol_significand = 0
#                     else: 
#                         total_vol_significand = ele.total_volume.significand
#                         
#                     res.append(
#                         (ele.scaled_open_price, ele.scaled_high_price, 
#                          ele.scaled_low_price, ele.scaled_close_price,
#                          total_vol_exponent, 
#                          total_vol_significand, price_scale
#                          )
#                         )
#     return res
# 
# =============================================================================
