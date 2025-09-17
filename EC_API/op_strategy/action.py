#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
from EC_API.op_strategy.enum import ActionStatus
from EC_API.payload.base import Payload

class ActionNode:
    def __init__(self, payload: Payload, on_filled = None, on_failed = None):
        self.payload: Payload = payload
        self.status: ActionStatus = ActionStatus.PENDING
        self.on_filled: ActionNode | None = on_filled
        self.on_failed: ActionNode | None = on_failed
        self.remark: str = ""
        
    def update(self):
        pass
    
class ActionTree:
    def __init__(self, root: ActionNode):
        pass