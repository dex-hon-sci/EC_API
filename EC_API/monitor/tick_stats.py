#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 09:27:21 2025

@author: dexter
"""
import numpy as np
from collections import deque
# EC_API imports
from EC_API.monitor.tick import Tick

ALL_STATS = { # Add more functions in the future
    "mean_price": lambda prices: float(np.mean(prices)),
    "std_price": lambda prices: float(np.std(prices, ddof=1)) if len(prices) > 1 else 0.0,
    "ohlc": lambda prices: {
        "open": float(prices[0]),
        "high": float(np.max(prices)),
        "low":  float(np.min(prices)),
        "close": float(prices[-1])
        },
    "mean_volume": lambda volumes: float(np.mean(volumes)),
    "std_volume": lambda volumes: float(np.std(volumes, ddof=1)) if len(volumes) > 1 else 0.0,
    "vwap": lambda prices, volumes: float(np.sum(prices * volumes) / np.sum(volumes)) if np.sum(volumes) > 0 else 0.0,
    }


class TickBufferStat:
    def __init__(self, keywords: list[str]=[]):
        self.stats: dict = {}
        
        self.price_stats: dict = {}
        self.volume_stats: dict = {}
        self.cross_stats: dict = {}
        
        if len(keywords)==0: 
            keywords = list(ALL_STATS.keys())
        
        # Build master dictionary with custom Stats drawn from ALL_STATS
        for keyword in keywords:
             if ALL_STATS.get(keyword) is not None:
                 if "price" in keyword:
                     self.price_stats[keyword] = ALL_STATS[keyword]
                 elif "volume" in keyword:
                     self.volume_stats[keyword] = ALL_STATS[keyword]
                 else:
                     self.cross_stats[keyword] = ALL_STATS[keyword]
    
    def compute(self, ticks: deque[list[Tick]]) -> dict[str, float]:
        """
        Compute statistics for a list of Tick objects.
        Returns a dictionary of stats.
        """
        if not ticks:
            return {}

        prices = np.array([t.price for t in ticks])
        volumes = np.array([t.volume for t in ticks])
        cross = np.array([(price, volume) for price, volume in zip(prices, volumes)])

        price_stats = {method(prices) for method in self.price_stats}
        volume_stats = {method(volumes) for method in self.volume_stats}
        cross_stats = {method(cross) for method in self.cross_stats}
        
        stats = {**price_stats, **volume_stats, **cross_stats}
        return stats