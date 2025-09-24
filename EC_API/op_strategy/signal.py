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
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)}        self.actions: ActionTree = actions
        self.start_time = start_time
        self.end_time = end_time
        
        self.context = ActionContext(self.start_time, self.end_time,self.feeds)
        self.status: OpSignalStatus = OpSignalStatus.ACTIVE
        
    def _make_payloads(self) -> None:
        pass
    
    def activate(self):
        self.status = OpSignalStatus.ACTIVE
        payload = self._make_payload()
        print(f"[OpSignal] Activated with payload {payload}")
        return payload

    def deactivate(self):
        self.status = OpSignalStatus.EXPIRED
        print(f"[OpSignal] Deactivated")
        
    #def _activation_logic(self) -> bool:
    #    pass
    
    #def _deactivate_logic(self) -> bool:
    #    pass
        
    def on_tick(self, price: float, volume: float, timestamp: float):
        self.context.update_market(price, volume, timestamp)
        self.action_tree.step(self.context)
    
    def run(self, now: datetime):
        if self.status == OpSignalStatus.PENDING and now >= self.context.start_time:
            return self.activate()
        elif self.status == OpSignalStatus.ACTIVE and now > self.context.end_time:
            self.deactivate()
            
    # decay_func, confidence level
