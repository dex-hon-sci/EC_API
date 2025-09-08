#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:32:34 2025

@author: dexter
"""
from collections import deque
from dataclasses import dataclass
import time
import numpy as np
import asyncio
from EC_API.monitor.tick_stats import ALL_STATS

@dataclass
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
        
        self.price_buffers = {tf: deque() for tf in self.timeframes}
        self.volume_buffers = {tf: deque() for tf in self.timeframes}
        self.timestamp_buffers = {tf: deque() for tf in self.timeframes}

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
            
