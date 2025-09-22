#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
from EC_API.op_strategy.enum import ActionStatus
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.ordering.base import LiveOrder

class ActionNode:
    def __init__(self, 
                 payloads: list[Payload], 
                 on_filled = None, 
                 on_failed = None):
        self.payloads: list[Payload] = payloads  # Each action can contain multiple Payload
        self.status: ActionStatus = ActionStatus.PENDING
        self.on_filled: ActionNode | None = on_filled
        self.on_failed: ActionNode | None = on_failed
        self.remark: str = ""
        
        self.trigger_cond = None
        
        self.connect: str = ""
        self.account_id: str = ""
        self.live_order: LiveOrder = LiveOrder()
        
    def check_trigger(self)->bool:
        if self.state == ActionStatus.PENDING and self.trigger_cond:
            return self.trigger_cond()
        return False
    
    def activate(self) -> None:
        for payload in self.payloads:
            print(payload)
            ###
            #EP = ExecutePayload(self.connect, payload, self.account_id, 
            #                    live_order=self.live_order).unload()
            
    def update_status(self, new_status: ActionStatus):
        self.status = new_status
        if new_status == ActionStatus.FILLED:
            return self.on_filled
        elif new_status == ActionStatus.VOID:
            return self.on_failed
        return None
    

class ActionTree:
    def __init__(self, root: ActionNode):
        self.cur = root
        
    def step(self) -> None:
        if not self.cur:
            return 
        if self.cur.check_trigger():
            self.cur.activate()