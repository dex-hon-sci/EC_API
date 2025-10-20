#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:19:23 2025

@author: dexter
"""

from typing import Protocol
from datetime import datetime
from EC_API.monitor.data_feed import DataFeed
from EC_API.op_strategy.enums import OpSignalStatus
from EC_API.op_strategy.action import ActionTree, ActionContext

class OpSignal(Protocol):
    """
    OpSignal contain the cool-down mechanism.
    """
    def __init__(self, 
                 feeds: dict[str, DataFeed],
                 action_tree: ActionTree,
                 start_time: datetime,
                 end_time: datetime):
        self.signal_id: str = ""
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)} 
        self.action_tree = action_tree
        self.start_time = start_time
        self.end_time = end_time
        
        self.context = ActionContext(self.start_time, self.end_time, self.feeds)
        self.status: OpSignalStatus = OpSignalStatus.INACTIVE
            
        # Creation, status Inactive,
        # If start_time is hit, activate, start running on_tick, that         
        # monitor raw data, time, price, volume
        # check the current node in the action tree, if it is exahusted,
        # change status to TERMINAL
        # If end_time is hit, EXPIRED
        
    def activate(self):
        self.status = OpSignalStatus.ACTIVE
        print("[OpSignal] Activated")
        
    def terminate(self):
        self.status = OpSignalStatus.TERMINAL
        print("[OpSignal] Terminated")

    def deactivate(self):
        self.status = OpSignalStatus.EXPIRED
        print("[OpSignal] Deactivated")
        

    def on_tick(self, price: float, volume: float, timestamp: float):
        self.context.update_market(price, volume, timestamp)
        self.action_tree.step(self.context)
    
    def run(self, now: datetime):
        
        self.on_tick()
        
        # During Active Signal
        if self.status == OpSignalStatus.PENDING and now >= self.context.start_time:
            return self.activate()
        elif not self.action_tree.cur:
            self.terminate()
        
        # When end_time is reached, override all status
        if self.status == OpSignalStatus.ACTIVE and now > self.context.end_time:
            self.deactivate()
            
    # decay_func, confidence level
