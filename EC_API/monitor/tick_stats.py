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
        
        self.storage: dict = {key: None for key in self.calculators}
        
    def stats(self, 
              horizon: float | None = None, 
              current_time: float | None = None) -> dict[str, None|int|float]:
        """
        Compute stats over either the whole buffer or a time-filtered window.
        Enforce minimum sample size.
        """
        prices, volumes, timestamps = self.buffer.get_window(horizon, current_time)
        n = len(prices)

        self.storage['n'] = n #{"n": n}  # always include sample size

        if n < self.min_n:
            # Too few ticks → mark stats as None/NaN
            for name in self.calculators.keys():
                self.storage[name] = None
            return self.storage

        for name, calc in self.calculators.items():
            self.storage[name] = calc.compute(prices, volumes, timestamps)

        return self.storage
