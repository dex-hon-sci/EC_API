#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 13:25:47 2025

@author: dexter
"""
from numpy import np
from typing import Protocol

class StatCalculator(Protocol):
    def compute(self, 
                prices: np.ndarray,
                volumes: np.ndarray, 
                timestamps: np.ndarray) -> float: pass
    @property
    def name(self) -> str: ...

class MeanPrice:
    name = "mean_price"
    def compute(self, prices, volumes, timestamps):
        return np.mean(prices) if prices.size > 0 else np.nan

class StdPrice:
    name = "std_price"
    def compute(self, prices, volumes, timestamps):
        return np.std(prices) if prices.size > 0 else np.nan
    
class MeanVolume:
    name = "mean_volume"
    def compute(self, prices, volumes, timestamps):
        return np.mean(prices) if prices.size > 0 else np.nan

class StdVolume:
    name = "std_volume"
    def compute(self, prices, volumes, timestamps):
        return np.std(prices) if prices.size > 0 else np.nan

class VWAP:
    name = "vwap"
    def compute(self, prices, volumes, timestamps):
        if volumes.sum() > 0:
            return float(np.sum(prices * volumes) / np.sum(volumes))
        return np.nan

class OHLC:
    def __init__(self): 
        self.name = "ohlc"
        
    def compute(self, prices, volumes, timestamps):
        if prices.size == 0:
            return None
        return {
            "open": prices[0],
            "high": np.max(prices),
            "low": np.min(prices),
            "close": prices[-1]
        }
    