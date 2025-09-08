#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 18:58:16 2025

@author: dexter
"""

# EC_API imports
from EC_API.monitor.tick import TickBuffer
from EC_API.monitor.tick_stats import TickBufferStat
    
class DataFeed:
    """ 
    DataFeed is a container class. It does not modify the behaviours/data of ticks.
    
    Standard: One Data Feed object contains only one TickBuffer and one set of 
    Stats. This is mainly a format class.
    
    Monitor object modify tickbuffer and tickbuffer stat. The DataFeed is a 
    container class. So the tick_buffer attributes will change accordingly.
    
    DataFeed is meant to be taken by OpStrategy for trade logic calculation.
    """
    def __init__(self, 
                 tick_buffer: TickBuffer,
                 tick_buffer_stat: TickBufferStat,
                 symbol: str = "",
                 ):
        self.tick_buffer: TickBuffer = tick_buffer
        self.tick_buffer_stat: dict = tick_buffer_stat.compute(self.tick_buffer)
        self.symbol: str = symbol


class CrossDataFeed: # WIP
    """
    An Object that process dervied data from more than one DataFeed. For 
    example, cross correlation of two different assets.
    
    CrossDataFeed is meant to be taken by OpStrategy for trade logic calculation
    """
    pass