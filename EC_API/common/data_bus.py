#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:51:23 2026

@author: dexter
"""

from typing import Callable
from EC_API.common.data_feeds import DataFeed


class DataBus:
    def __init__(self):
        self._registered_feeds: dict[int, list[DataFeed]] = dict()  # contract_id-> list
        self._callbacks: dict[int, list[Callable]] = dict()  # contract_id-> list

    def register(
        self, contract_id: int, feed: DataFeed, on_tick: Callable[[int], None]
    ) -> None: ...

    def deregister(
        self, contract_id: int, feed: DataFeed, on_tick: Callable[[int], None]
    ) -> None: ...

    def push(self, raw: tuple) -> None: ...

    def __init__(self):
        _registry: dict[str, dict[str, tuple[DataFeed, Callable]]]
        # symbol -> {feed_id -> (feed, callback)}

    def register(self, symbol: str, feed_id: str, feed: DataFeed, on_tick: Callable) -> None:
        self._registry.setdefault(symbol, {})[feed_id] = (feed, on_tick)
  
    def deregister(self, symbol: str, feed_id: str) -> None:
        self._registry[symbol].pop(feed_id, None)
  
    def push(self, symbol: str, raw: tuple) -> None:
        for feed, cb in self._registry.get(symbol, {}).values():
            feed.update(raw)
            cb(symbol)
