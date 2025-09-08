#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:19:23 2025

@author: dexter
"""

from typing import Protocol
from EC_API.monitor.data_feed import DataFeed
from EC_API.op_strategy.signal 

class OpSignal(Protocol):
    """
    OpSignal contain the cool-down mechanism.
    Input: DataFeed
    Output: Payload
    """
    def __init__(self, 
                 datafeed_pool: list[DataFeed],
                 payload_pool: list[DataFeed]):
        self.datafeed_pool = datafeed_pool
        self.payload_pool = payload_pool
        self.status: 
        
    def _make_payloads(self) -> None:
        pass
        
    def _activation_logic(self) -> bool:
        """Siganl Activation Logic goes here."""
        pass
    
    def _deactivate_logic(self) -> bool:
        pass
    
    def _insert_payload(self) -> None:
        """Insert Payload into Storage Table of the DB."""
        pass
    
    def run(self):
        if self._activation_logic():
            self._insert_payload()
            pass

    # start_time, end_time    
    # decay_func, confidence level
    # 
