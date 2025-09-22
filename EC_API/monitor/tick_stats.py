#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:27:21 2025

@author: dexter
"""
import numpy as np
from collections import deque
# EC_API imports
from EC_API.monitor.tick import TickBuffer
from EC_API.utility.base import time_it

    
class TickBufferStat:
    def __init__(self, 
                 buffer: TickBuffer, 
                 calculators: dict[str, object], 
                 min_n: int = 10):
        """
        :param buffer: TickBuffer instance
        :param calculators: dict of StatCalculator objects
        :param min_n: minimum sample size required to compute stats
        """
        self.buffer = buffer
        self.calculators = calculators
        self.min_n = min_n

    def stats(self, 
              horizon: float | None = None, 
              current_time: float | None = None) -> dict[str, None|int|float]:
        """
        Compute stats over either the whole buffer or a time-filtered window.
        Enforce minimum sample size.
        """
        prices, volumes, timestamps = self.buffer.get_window(horizon, current_time)
        n = len(prices)

        result = {"n": n}  # always include sample size

        if n < self.min_n:
            # Too few ticks → mark stats as None/NaN
            for name in self.calculators.keys():
                result[name] = None
            return result

        for name, calc in self.calculators.items():
            result[name] = calc.compute(prices, volumes, timestamps)

        return result
    
# =============================================================================
# ALL_STATS = { # Add more functions in the future
#     "mean_price": lambda prices: float(np.mean(prices)),
#     "std_price": lambda prices: float(np.std(prices, ddof=1)) if len(prices) > 1 else 0.0,
#     "ohlc_price": lambda prices: {
#         "open": float(prices[0]),
#         "high": float(np.max(prices)),
#         "low":  float(np.min(prices)),
#         "close": float(prices[-1])
#         },
#     "mean_volume": lambda volumes: float(np.mean(volumes)),
#     "std_volume": lambda volumes: float(np.std(volumes, ddof=1)) if len(volumes) > 1 else 0.0,
#     "vwap": lambda prices, volumes: float(np.sum(prices * volumes) / np.sum(volumes)) if np.sum(volumes) > 0 else 0.0,
#     }
# 
# 
# class TickBufferStat:
#     def __init__(self, keywords: list[str]=[]):
#         self.stats: dict = {}
#         
#         self.price_stats: dict = {}
#         self.volume_stats: dict = {}
#         self.cross_stats: dict = {}
#         
#         if len(keywords)==0: 
#             keywords = list(ALL_STATS.keys())
#         #print("keyword_create", keywords)
#         
#         # Build master dictionary with custom Stats drawn from ALL_STATS
#         for keyword in keywords:
#              if ALL_STATS.get(keyword) is not None:
#                  print('keyword', keyword)
#                  if "price" in keyword:
#                      self.price_stats[keyword] = ALL_STATS[keyword]
#                  elif "volume" in keyword:
#                      self.volume_stats[keyword] = ALL_STATS[keyword]
#                  else:
#                      self.cross_stats[keyword] = ALL_STATS[keyword]
#                      
#     @time_it
#     def compute(self, ticks: deque[list[Tick]]) -> dict[str, float]:
#         """
#         Compute statistics for a list of Tick objects.
#         Returns a dictionary of stats.
#         """
#         if not ticks:
#             return {}
#         #print("self.price_stats", self.price_stats)
#         #print("self.volume_stats", self.volume_stats)
#         #print("self.cross_stats", self.cross_stats)
#         
#         prices = np.array([t.price for t in ticks])
#         volumes = np.array([t.volume for t in ticks])
#         #cross = np.array([(price, volume) for price, volume in zip(prices, volumes)])
# 
#         price_stats = {method:self.price_stats[method](prices) for method in self.price_stats}
#         volume_stats = {method:self.volume_stats[method](volumes) for method in self.volume_stats}
#         cross_stats = {method:self.cross_stats[method](prices, volumes) for method in self.cross_stats}
#         
#         stats = {**price_stats, **volume_stats, **cross_stats}
#         #print("stats", stats)
#         return stats
# =============================================================================
