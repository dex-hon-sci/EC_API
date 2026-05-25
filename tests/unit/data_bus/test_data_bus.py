#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:47:56 2026

@author: dexter
"""
import pytest
from EC_API.common.data_feeds import DataFeed, CrossFeeds
from EC_API.common.data_bus import DataBus
from EC_API.exceptions import DataBusRegisterError


def test_data_bus_register_valid_datafeed() -> None:
    DB = DataBus()
    df = DataFeed()
    
    DB.register("symbol_1", "feed_id_1", df, None)
    
    assert DB.registry.get("symbol_1")
    assert DB.registry["symbol_1"].get("feed_id_1")
    assert DB.registry["symbol_1"]["feed_id_1"] == (df, None)
    
def test_data_bus_register_valid_crossfeeds() -> None:
    DB = DataBus()
    cf = CrossFeeds()
    
    DB.register("symbol_1", "feed_id_1", cf, None)
    
    assert DB.registry.get("symbol_1")
    assert DB.registry["symbol_1"].get("feed_id_1")
    assert DB.registry["symbol_1"]["feed_id_1"] == (cf, None)

    
def test_data_bus_register_invalid_wrong_symbol_type() -> None:
    DB = DataBus()
    df = DataFeed()
    with pytest.raises(TypeError):
        DB.register(1, "feed_id_1", df, None) # <--- Wrong symbol type

def test_data_bus_register_invalid_wrong_feed_id_type() -> None:
    DB = DataBus()
    df = DataFeed()
    with pytest.raises(TypeError):
        DB.register("symbol_1", 1, df, None) # <--- Wrong feedid type
        
def test_data_bus_register_invalid_wrong_data_feed_type() -> None:
    DB = DataBus()
    with pytest.raises(DataBusRegisterError):
        DB.register("symbol_1", "feed_id_1", [], None) # <--- Wrong datafeed type

def test_data_bus_register_invalid_wrong_callback_type() -> None:
    DB = DataBus()
    with pytest.raises(DataBusRegisterError):
        DB.register("symbol_1", "feed_id_1",  DataFeed(), 0) # <--- Wrong callback type


def test_data_bus_deregister_valid() -> None:
    DB = DataBus()
    df1, df11, df2, df3 = DataFeed(), DataFeed(),  DataFeed(), DataFeed()
    
    DB.register("symbol_1", "feed_id_1", df1, None)
    DB.register("symbol_1", "feed_id_11", df11, None)
    DB.register("symbol_2", "feed_id_2", df2, None)
    DB.register("symbol_3", "feed_id_3", df3, None)
    
    DB.deregister("symbol_1", "feed_id_1")
    DB.deregister("symbol_3", "feed_id_3")
    
    assert 'symbol_1' in DB.registry.keys()
    assert 'symbol_2' in DB.registry.keys()
    assert 'symbol_3' not in DB.registry.keys()
    
    assert "feed_id_1" not in DB.registry['symbol_1'].keys()
    
    
def test_data_bus_deregister_invalid_wrong_symbol() -> None:
    DB = DataBus()
    df = DataFeed()

    DB.register("symbol_1", "feed_id_1", df, None)

    with pytest.raises(DataBusRegisterError):
        DB.deregister("symbol_2", "feed_id_1") #<--- wrong symbol
        
def test_data_bus_deregister_invalid_wrong_feed_id() -> None:
    DB = DataBus()
    df = DataFeed()

    DB.register("symbol_1", "feed_id_1", df, None)

    with pytest.raises(DataBusRegisterError):
        DB.deregister("symbol_1", "feed_id_2") #<--- wrong symbol
