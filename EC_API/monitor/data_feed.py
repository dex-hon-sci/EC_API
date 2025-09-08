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
# EC_API imports
from EC_API.monitor.tick import TickBuffer, TickBufferStat
    
class DataFeed: # WIP
    """ 
    Standard: One Data Feed object contains only one TickBuffer and one set of 
    Stats. This is mainly a forat class.
    
    Monitor object modify tickbuffer and tickbuffer stat. The DataFeed is a 
    container class. So the tick_buffer attributes will change accordingly.
    
    
    DataFeed is meant to be taken by OpStrategy for trade logic calculation.
    """
    def __init__(self, 
                 tick_buffer: TickBuffer,
                 symbol: str = ""):
        self.tick_buffer: TickBuffer = tick_buffer
        self.tick_buffer_stat: dict = TickBufferStat().compute(self.tick_buffer)
        self.symbol: str = symbol
    

class CrossDataFeed: # WIP
    """
    An Object that process dervied data from more than one DataFeed. For 
    example, cross correlation of two different assets.
    
    CrossDataFeed is meant to be taken by OpStrategy for trade logic calculation
    """
    pass