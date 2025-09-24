#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
from typing import Callable, Optional, Any, field
from dataclasses import dataclass
from datetime import datetime
from EC_API.op_strategy.enum import ActionStatus
from EC_API.op_strategy.data_feed import DataFeed
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.ordering.base import LiveOrder


class ActionContext:
    def __init__(self, 
                 start_time: datetime, 
                 end_time: datetime,
                 feeds: dict[str, DataFeed],):
        self.start_time = start_time
        self.end_time = end_time
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)}        self.actions: ActionTree = actions
        
        self.connect: str = ""
        self.account_id: str = ""
        self.live_order: LiveOrder = LiveOrder()    
    
    def update_market(self, price: float, volume: float, timestamp: datetime):
        self.data.update({
            "price": price,
            "volume": volume,
            "timestamp": timestamp,
        })

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set_(self, key: str, value: Any):
        self.data[key] = value
        
        
class ActionNode:
    def __init__(self, 
                 payloads: list[Payload], 
                 trigger_cond: Callable,
                 on_filled = None, 
                 on_failed = None,
                 on_overtime = None,
                 remark: str =""):
        self.payloads: list[Payload] = payloads  # Each action can contain multiple Payload
        self.status: ActionStatus = ActionStatus.PENDING
        self.on_filled: ActionNode | None = on_filled
        self.on_failed: ActionNode | None = on_failed
        self.on_overtime: ActionNode | None = on_overtime
        self.remark: str = remark
        
        self.trigger_cond: Callable | None = trigger_cond
        
        self.connect: str = ""
        self.account_id: str = ""
        self.live_order: LiveOrder = LiveOrder()
        
    #def evaluate(self, ctx)->bool:
    #    if not self.state == ActionStatus.PENDING:
    #        return False
    #    else:
    #        if self.trigger_cond:
    #            return self.trigger_cond()
    def evaluate(self, ctx: dict) -> Optional["ActionNode"]:
        # Only evaluate nodes that are still pending
        if self.state != ActionStatus.PENDING:
            return None

        if self.condition(ctx):
            print(f"[ActionNode] {self.name} triggered.")
            self.state = ActionStatus.ACTIVE

            if self.action:
                try:
                    self.action(ctx)
                    self.state = ActionStatus.COMPLETED
                except Exception as e:
                    print(f"[ActionNode] {self.name} failed: {e}")
                    self.state = ActionStatus.FAILED

            # Once this node is completed, check children
            for child in self.children:
                nxt = child.evaluate(ctx)
                if nxt:
                    return nxt
        return None
    
    def activate(self) -> None:
        for payload in self.payloads:
            try:
                print(payload)
                #EP = ExecutePayload(self.connect, payload, self.account_id, 
                #                    live_order=self.live_order).unload()
            except:
                pass
            
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
        self.root = root
        
# =============================================================================
#     def step(self) -> None:
#         if self.cur is not None:
#             if self.cur.check_trigger():
#                 self.cur.activate()
# =============================================================================
    def finished(self)-> bool:
        return self.cur is None

    def step(self, ctx: dict) -> None:
        # ctx: ActionContext
        # Check global timeout
        if "end_time" in ctx and ctx["now"] > ctx["end_time"] and self.overtime_node:
            print("[ActionTree] Timeout reached → overtime branch.")
            self.cur = self.overtime_node

        if self.cur and self.cur.state == ActionStatus.PENDING:
            nxt = self.current.evaluate(ctx)
            if nxt:
                self.current = nxt
        