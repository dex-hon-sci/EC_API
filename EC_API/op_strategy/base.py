#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 12:52:55 2025

@author: dexter

Operational Strategy module
"""
from typing import Protocol
# EC_APi imports
from EC_API.monitor.data_feed import DataFeed

class OpStrategy(Protocol):
    """
    Base class of Operational Strategy
    
    Input: Monitor info, specify data type, sizes and x.
    DB_address: somewhere to save the outputs
    Output: OpSignal. 
    """
    def __init__(self,
                 datafeed_pool: list[DataFeed],
                 payload_pool: list[DataFeed]):
        self.datafeed_pool = datafeed_pool
        self.payload_pool = payload_pool
        
    def on_tick():
        pass
    
    def insert_signal():
        pass
        
class ActionNode(Protocol):
    pass

class ActionTree(Protocol):
    pass
        
