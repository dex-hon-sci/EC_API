#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 01:06:27 2026

@author: dexter
"""
from typing import Any, Iterable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.protocol.cqg.key_extractors import walk_fields
# contract_id, OHLC, volume_significand, volume_exponent, volume_significand
MarketValueType = tuple[str, int, int, int, int, int] 

def parse_real_time_market_data2(server_msg: ServerMsg)-> list[dict[str,Any]]:
    # Need to walk through the message
    res = []
    if server_msg.real_time_market_data:
        real_time_market_data = server_msg.real_time_market_data
        for data in real_time_market_data:
            if real_time_market_data:
                for ele in data.market_values:
                    if not ele.total_volume.exponent:
                        total_vol_exponent = 0
                    else: 
                        total_vol_exponent = ele.total_volume.exponent
                        
                    if not ele.total_volume.significand:
                        total_vol_significand = 0
                    else: 
                        total_vol_significand = ele.total_volume.significand
                    res.append(
                        (ele.scaled_open_price, ele.scaled_high_price, 
                         ele.scaled_low_price, ele.scaled_close_price,
                         total_vol_exponent, 
                         total_vol_significand
                         )
                        )
    return res


def parse_real_time_market_data(server_msg: ServerMsg) -> list[MarketValueType]:
    TARGET = {
        "market_values",
        "quote"
        }
    
    def selector(fd, val) -> Iterable[Any]:
        if fd.message_type is not None and fd.name == "real_time_market_data":
            yield 
        else:
            yield
        
    outs = walk_fields(server_msg, selector, max_depth=1)

    return outs

def parse_order_statuses_data(server_msg: ServerMsg)-> dict[str,Any]:
    return 