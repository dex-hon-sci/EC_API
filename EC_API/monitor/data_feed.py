#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 18:58:16 2025

@author: dexter
"""
from collections import deque
from dataclasses import dataclass
import time
import numpy as np
import asyncio

class Tick:
    price: int
    volume: int
    timestamp: int  # Unix timestamp
    
class TickBuffer:
    def __init__(self, timeframes_seconds: int | float):
        """
        timeframes_seconds: single float or list of floats for 
        multi-timeframe buffers
        """
        if isinstance(timeframes_seconds, (int, float)):
            timeframes_seconds = [timeframes_seconds]
        self.timeframes = timeframes_seconds
        self.buffers = {tf: deque() for tf in self.timeframes}

    def add_tick(self, 
                 price: int, 
                 volume: int, 
                 timestamp: int = None):
        if timestamp is None:
            timestamp = time.time()
        tick = Tick(price, volume, timestamp)
        for tf, buf in self.buffers.items():
            buf.append(tick)
            self._pop_old_ticks(buf, tf, timestamp)

    def _pop_old_ticks(self, buf, 
                       timeframe: float, 
                       current_time: float):
        """Remove ticks older than timeframe"""
        while buf and buf[0].timestamp < current_time - timeframe:
            buf.popleft()
            
    def _select_buffer(self, tf):
        if tf is None:
            tf = self.timeframes[0]
        return self.buffers[tf]
            
    def ohlc(self, tf=None):
        buf = self._select_buffer(tf)
        if not buf:
            return None
        prices = [t.price for t in buf]
        return {
            "Open": prices[0],
            "High": max(prices),
            "Low": min(prices),
            "Close": prices[-1]
            }

    def size(self, tf=None):
        buf = self._select_buffer(tf)
        return len(buf)

    def clear(self, tf=None):
        if tf is None:
            for buf in self.buffers.values():
                buf.clear()
        else:
            self.buffers[tf].clear()

class TickBufferStat:
    def compute(self, ticks: list[Tick]) -> dict[str, float]:
        """
        Compute statistics for a list of Tick objects.
        Returns a dictionary of stats.
        """
        if not ticks:
            return {}

        prices = np.array([t.price for t in ticks])
        volumes = np.array([t.volume for t in ticks])

        stats = {
            "mean_price": float(np.mean(prices)),
            "std_price": float(np.std(prices, ddof=1)) if len(prices) > 1 else 0.0,
            "mean_volume": float(np.mean(volumes)),
            "std_volume": float(np.std(volumes, ddof=1)) if len(volumes) > 1 else 0.0,
            "vwap": float(np.sum(prices * volumes) / np.sum(volumes)) if np.sum(volumes) > 0 else 0.0,
            "ohlc": {
                "open": float(prices[0]),
                "high": float(np.max(prices)),
                "low": float(np.min(prices)),
                "close": float(prices[-1])
            }
        }
        return stats