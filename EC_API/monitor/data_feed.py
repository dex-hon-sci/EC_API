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
                 buf_stat_method: TickBufferStat = TickBufferStat(),
                 symbol: str = "",
                 ):
        self.tick_buffer: TickBuffer = tick_buffer
        self.symbol: str = symbol
        
        self.buf_stat_method: TickBufferStat= buf_stat_method
        self._tick_buffer_stat: dict = {}

    @property
    def tick_buffer_stat(self): # Only Getter method is needed in this class
        print("TICK BUF STAT", self.tick_buffer.buffers, type(self.tick_buffer.buffers))

        for buffer_key in self.tick_buffer.buffers:
            print("BUF KEY",buffer_key, self.tick_buffer.buffers[buffer_key], 
                  type(self.tick_buffer.buffers[buffer_key]))
            self._tick_buffer_stat[buffer_key] = self.buf_stat_method.compute(
                                                 self.tick_buffer.buffers[buffer_key])
            return self._tick_buffer_stat

class CrossDataFeed: # WIP
    """
    An Object that process dervied data from more than one DataFeed. For 
    example, cross correlation of two different assets.
    
    CrossDataFeed is meant to be taken by OpStrategy for trade logic calculation
    """
    pass