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
