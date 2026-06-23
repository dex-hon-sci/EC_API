#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 18:58:16 2025

@author: dexter
"""
from typing import Union, Any
from dataclasses import dataclass, asdict

#from EC_API.common.tick import TickBuffer
from EC_API.common.tick_stats import TickBufferStat
from EC_API.common.tick_buffers_ext import (
    SlidingWindowBuffer, RingBuffer, 
    DataExtractionPolicy, 
    StatType
    )
from EC_API.common.tick_buffers_ext import StatConfig as CPPStatConfig

type TickBuffer = Union[SlidingWindowBuffer, RingBuffer]
default_buf = SlidingWindowBuffer(DataExtractionPolicy.ExtractTradeTickCQG, 10.0,0.0)

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
    # Data Engine holds a dict for (current_symbol_name<->long_term_symbol_name)
    # stream_name is the long term name
    # DataFeed only care for the long term nanme
    def __init__(
        self,
        symbol: str = "",
        tick_buffer: TickBuffer = default_buf,
        stat_config: CPPStatConfig = CPPStatConfig(),
    ):
        # Buffers
        #self._ring_price: list = []  # np.ndarray  shape (window,)
        #self._ring_time: list = []  # np.ndarray  shape (window,)
        #self._ptr: int = 0

        # Configs
        self.stat_config: CPPStatConfig = stat_config
        self.cpp_stat_config = stat_config
        self.cpp_buffer = tick_buffer # only one buffer per DataFeed

        self.symbol: str = symbol
        self.stat_snapshot: dict[str,tuple[Any]] = dict() # update

        #self.tick_buffer: TickBuffer = tick_buffer
        #self.min_n: int = min_n
        #self.calculators: dict = calculators
        #self.buf_stat_method: TickBufferStat = TickBufferStat(
        #    self.tick_buffer, calculators=self.calculators, min_n=self.min_n
        #)
        # ----
        
    def get_stat_snapshot(self, stat_name: StatType) -> tuple:
        return self.cpp_buffer.get_stat_snapshot(stat_name)
            
    def update(self, raw: tuple) -> None: # main methods to updates all attribute and statistics
        # add tick, compute new stat, tick eviction
        self.cpp_buffer.add_tick(raw)

# =============================================================================
#       def update(self, raw: tuple) -> None:
#           ts, price, vol = raw          # or vendor-specific unpacking
#           self._buffer.add_tick(ts, price, vol)
#           self._snap = self._buffer.stats   # cached, O(1)
# 
#       @property
#       def snapshot(self) -> FeedSnapshot:
#           return self._snap
# 
#   Strategy side:
# 
#   def on_tick(symbol: str) -> None:    # this IS the DataBus callback
#       snap = feed.snapshot
#       if snap.vwap > snap.mean_price * 1.002:
#           ...
# =============================================================================
# =============================================================================
# 
#   class SlidingWindowBuffer:
#       def __init__(self, window_seconds: float):
#           self._window = window_seconds
#           self._ticks: deque[Tick] = deque()   # time-ordered
#           self._acc = RunningAccumulator()     # single object, all running sums
# 
#       def add_tick(self, ts: float, price: float, vol: float) -> None:
#           # 1. expire old ticks first (subtract from acc)
#           cutoff = ts - self._window
#           while self._ticks and self._ticks[0].timestamp < cutoff:
#               old = self._ticks.popleft()
#               self._acc.remove(old.price, old.volume)
#           # 2. add new tick
#           t = Tick(price, vol, ts)
#           self._ticks.append(t)
#           self._acc.add(price, vol)
# 
#       @property
#       def stats(self) -> AccumulatorSnapshot:
#           return self._acc.snapshot()    # returns a NamedTuple, O(1)
# =============================================================================
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
# =============================================================================
#   Strategy side:
# 
#   def on_tick(symbol: str) -> None:    # this IS the DataBus callback
#       snap = feed.snapshot
#       if snap.vwap > snap.mean_price * 1.002:
#           ...
# 
# 
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
