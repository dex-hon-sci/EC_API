#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:51:23 2026

@author: dexter
"""

from typing import Callable
from EC_API.common.data_feeds import DataFeed
from EC_API.exceptions import DataBusRegisterError

class DataBus:
    # Registeration for feeds by id
    # dispatch to each consumers
    # DataFeed handle ticks statistics and vendor formatting
    # an Engine owns a DataBus
    def __init__(self):
        self._registry: dict[str, dict[str, tuple[DataFeed, Callable]]]
        # symbol -> {feed_id -> (feed, callback)}
        # Feed-id follows the format of strat_id+symbol
        
    def register(self, symbol: str, feed_id: str, feed: DataFeed, on_tick: Callable) -> None:
        if not isinstance(symbol, str) and isinstance(feed_id, str):
            raise TypeError(f"Both {symbol} and {feed_id} has to be str.")
        # check data feed
        if not isinstance(feed, DataFeed):
            raise DataBusRegisterError(f"feed:{feed} has to be of type 'DataFeed'")
        
        # check callbacks
        
        
        self._registry.setdefault(symbol, {})[feed_id] = (feed, on_tick)
  
    def deregister(self, symbol: str, feed_id: str) -> None:
        if symbol not in self._registry.keys():
            raise DataBusRegisterError(f"symbol: {symbol} not in DataBus's registry.")
        if feed_id not in self._registry[symbol].keys():
            raise DataBusRegisterError(f"feed_id:{feed_id} not in the entry of symbol:{symbol}.")
        # check active usage
        self._registry[symbol].pop(feed_id, None)
  
    def push(self, symbol: str, raw: tuple) -> None:
        for feed, cb in self._registry.get(symbol, {}).values():
            feed.update(raw)
            cb(symbol)
