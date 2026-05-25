#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 18:58:16 2025

@author: dexter
"""

from EC_API.common.tick import TickBuffer
from EC_API.common.tick_stats import TickBufferStat


class DataFeed:
    """
    DataFeed is a container class.

    DataFeed is meant to be taken by OpStrategy for trade logic calculation.
    """
    # Extract relevant data based on vendor (extractor and policy)
    # trasnform raw ticks into usable streaming data for OpSIgnala and OpStrategy
    # ID translation contract_id (0) -> symbol_name (CLEV26) -> stream_name (CLE)
    # symbol_registry in monitor object hold translation (symbol_name -> contract_id)
    # DataEngine calls MonitorData stream()
    # DataEngine runs broadcast_loop via channel.broadcast('stream_name', data)
    def __init__(
        self,
        tick_buffer: TickBuffer=[],
        calculators: dict = {},
        min_n: int = 20,
        symbol: str = "",
    ):
        self._ring_price: list = []  # np.ndarray  shape (window,)
        self._ring_time: list = []  # np.ndarray  shape (window,)
        self._ptr: int = 0

        self.tick_buffer: TickBuffer = tick_buffer
        self.symbol: str = symbol
        self.min_n: int = min_n
        self.calculators: dict = calculators
        self.buf_stat_method: TickBufferStat = TickBufferStat(
            self.tick_buffer, calculators=self.calculators, min_n=self.min_n
        )
        # ----
        self._latest = 0
        self._mean = 0
        self._std = 0
        self._median = 0

    # @property
    def tick_buffer_stat(self, horizon: float, current_time: float) -> dict[str, float | None]:
        # Only Getter method is needed in this class
        return self.buf_stat_method.stats(horizon, current_time)

    def latest(self) -> None:
        return self._latest

    @property
    def mean(self) -> float:
        return self._median

    @property
    def std(self) -> float:
        return

    def vwamp() -> float:
        ...
        
    def update(self) -> None: # main methods to updates all attribute and statistics
        ...


# =============================================================================
#     @property
#     def tick_buffer_stat(self): # Only Getter method is needed in this class
#         print("TICK BUF STAT", self.tick_buffer.buffers, type(self.tick_buffer.buffers))
#
#         for buffer_key in self.tick_buffer.buffers:
#             print("BUF KEY",buffer_key, self.tick_buffer.buffers[buffer_key],
#                   type(self.tick_buffer.buffers[buffer_key]))
#             self._tick_buffer_stat[buffer_key] = self.buf_stat_method.compute(
#                                                  self.tick_buffer.buffers[buffer_key])
#             return self._tick_buffer_stat
# buf_stat_method: TickBufferStat = TickBufferStat(
# buf_stat_method()
# self._tick_buffer_stat: dict = {}
# =============================================================================


class CrossFeeds:  # WIP
    """
    An Object that process dervied data from more than one DataFeed. For
    example, cross correlation of two different assets.

    CrossDataFeed is meant to be taken by OpStrategy for trade logic calculation
    """

    def __init__(self):
        self._feeds: dict[str, DataFeed] = dict()

    def spread(self, a: str, b: str) -> float:
        return

    def ratio(self, a: str, b: str) -> float:
        return

    def corr(self, a: str, b: str) -> float:
        return
