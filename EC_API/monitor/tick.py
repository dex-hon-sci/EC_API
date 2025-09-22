#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:32:34 2025

@author: dexter
"""
# Python imports
from typing import Protocol
from dataclasses import dataclass
from collections import deque
import time
# Python Package imports
import numpy as np
# EC_API imports
from EC_API.utility.base import time_it

@dataclass
class Tick:
    price: int
    volume: int
    timestamp: int  # Unix timestamp

class TickBuffer(Protocol):
    def __init__(self): pass
    def add_tick(self): pass
    def current_tick(self): pass
    
    
class RingTickBuffer(TickBuffer):
    def __init__(self, size:int):
        self.size = size
        self.prices = np.zeros(size, dtype=np.float64)
        self.volumes = np.zeros(size, dtype=np.float64)
        self.timestamps = np.zeros(size, dtype=np.float64)
        
        self.cur = 0
        self.full = False
        
    def add_tick(self, price: float, volume: float, timestamp: float) -> None:
        if timestamp is None:
            timestamp = time.time()
        self.prices[self.cur] = price
        self.volumes[self.cur] = volume
        self.timestamps[self.cur] = timestamp

        self.cur = (self.cur + 1) % self.size
        if self.cur == 0: #no reminder, array is full
            self.full = True

    def get_window(self, 
                   horizon: float | None = None,
                   current_time: float | None = None) -> tuple[np.array[int|float]]:
        """
        - If horizon is None → return last N ticks (tick-based window).
        - If horizon is given → filter ticks by time (time-based window).
        """
        if self.full:
            prices, vols, ts = self.prices, self.volumes, self.timestamps
        else:
            prices, vols, ts = self.prices[:self.cur], self.volumes[:self.cur], self.timestamps[:self.cur]
        
        if horizon is not None and current_time is not None:
            mask = ts >=current_time - horizon #filter condition in timestamp array
            return prices[mask], vols[mask], ts[mask]
        
    def __len__(self):
        return self.size if self.full else self.cur

    def current_tick(self) -> Tick | None:
        """Return the most recent tick as a Tick object."""
        if len(self) == 0:
            return None
        last_index = (self.cur - 1) % self.size
        return Tick(
            price=float(self.prices[last_index]),
            volume=float(self.volumes[last_index]),
            timestamp=float(self.timestamps[last_index]),
        )
    
class TimeTickBuffer(TickBuffer):
    def __init__(self, timeframes_seconds: int | float):
        """
        timeframes_seconds: single float or list of floats for 
        multi-timeframe buffers
        """
        if isinstance(timeframes_seconds, (int, float)):
            timeframes_seconds = [timeframes_seconds]
        self.timeframes = timeframes_seconds
        self.buffers = {tf: deque(np.array([])) for tf in self.timeframes}

    @time_it
    def add_tick(self, 
                 price: int, 
                 volume: int, 
                 timestamp: int = None) -> None:
        if timestamp is None:
            timestamp = time.time()
        tick = Tick(price, volume, timestamp)
        for tf, buf in self.buffers.items():
            buf.append(tick)
            self._pop_old_ticks(buf, tf, timestamp)
    @time_it
    def _pop_old_ticks(self, buf, 
                       timeframe: float, 
                       current_time: float) -> None:
        """Remove ticks older than timeframe"""
        while buf and buf[0].timestamp < current_time - timeframe:
            buf.popleft()
            
    def _select_buffer(self, tf) -> deque[np.array[float|int]]:
        if tf is None:
            tf = self.timeframes[0]
        return self.buffers[tf]
            
    def ohlc(self, tf=None) -> dict[str, float|int]:
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

    def size(self, tf=None) -> int:
        buf = self._select_buffer(tf)
        return len(buf)

    def clear(self, tf=None) -> None:
        if tf is None:
            for buf in self.buffers.values():
                buf.clear()
        else:
            self.buffers[tf].clear()
            
