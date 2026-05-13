#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:19:23 2025

@author: dexter
"""
from abc import ABC
from datetime import datetime
from EC_API.monitor.data_feed import DataFeed, CrossFeeds
from EC_API.op_strategy.enums import OpSignalStatus, OPSIGNAL_STATUS_LIFECYCLE
from EC_API.op_strategy.action import ActionTree, ActionContext
from EC_API.utility.state_mgr import StateMgr


class OpSignal(ABC):
    """
    OpSignal contain the cool-down mechanism.
    """
    def __init__(
            self, 
            feeds: dict[str, DataFeed],
            action_tree: ActionTree,
            start_time: datetime,
            end_time: datetime
        ):
        self.signal_id: str = ""
        
        self.feeds: dict[str, DataFeed] = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)} 
        self.cross: CrossFeeds = None
        
        self.action_tree = action_tree
        self.start_time = start_time
        self.end_time = end_time
        
        self.context = ActionContext(self.start_time, self.end_time, self.feeds)        

        self._state_mgr: StateMgr = StateMgr(
            OPSIGNAL_STATUS_LIFECYCLE, 
            OpSignalStatus.INACTIVE,
            OpSignalStatus.INACTIVE,
            allowed_starts = [OpSignalStatus.INACTIVE]
            )        


        # Creation, status Inactive,
        # If start_time is hit, activate, start running on_tick, that         
        # monitor raw data, time, price, volume
        # check the current node in the action tree, if it is exahusted,
        # change status to TERMINAL
        # If end_time is hit, EXPIRED
        
    # --- Internals ---
    @property
    def state(self) -> OpSignalStatus:
        return self._state_mgr.cur

    # --- Functions ---
    def activate(self):
        self.state = OpSignalStatus.ACTIVE
        print("[OpSignal] Activated")
        
    def terminate(self):
        self.state = OpSignalStatus.TERMINAL
        print("[OpSignal] Terminated")

    def deactivate(self):
        self.state = OpSignalStatus.EXPIRED
        print("[OpSignal] Deactivated")
        
    # ---
    def on_tick(
            self, 
            price: float, 
            volume: float, 
            timestamp: float
        ):
        self.context.update_market(price, volume, timestamp)
        self.action_tree.step(self.context)
    
    def run(self, now: datetime):
        
        self.on_tick()
        
        # During Active Signal
        if self.state == OpSignalStatus.PENDING and now >= self.context.start_time:
            return self.activate()
        elif not self.action_tree.cur:
            self.terminate()
        
        # When end_time is reached, override all status
        if self.state == OpSignalStatus.ACTIVE and now > self.context.end_time:
            self.deactivate()
            
    # decay_func, confidence level
