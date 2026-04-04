#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:35:02 2026

@author: dexter
"""
from EC_API.monitor.cqg.parsers import (
    parse_real_time_market_data,
    )
from tests.unit.fixtures.server_msg_streams_CQG import (
    build_real_time_market_data_server_msg,
    dummy_realtime_data_stream, 
    dummy_order_update_stream
    )
from EC_API._typing import MarketValueType

def test_parser_real_data_stream_valid() -> None:
    server_msg = build_real_time_market_data_server_msg()
    res = parse_real_time_market_data(server_msg)
    
    print(res)
    
    assert isinstance(res, list)
    assert len(res) == 2
    for ele in res:
        assert isinstance(ele,tuple)
    
    
    