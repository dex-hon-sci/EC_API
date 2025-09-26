#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
from typing import Callable, Optional, Any, field, Self
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
                 feeds: dict[str, DataFeed]):
        self.start_time = start_time
        self.end_time = end_time
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)}        self.actions: ActionTree = actions
        
        # Exchange specific attributes
        self.connect: str = ""
        self.account_id: str = ""
        self.live_order: LiveOrder = LiveOrder() # Specify LiveOrder type, such as CQGLiveOrder  
    
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
                 trigger_cond: Callable[ActionContext, dict],
                 payloads: list[Payload], # Payloads of this action
                 transitions: dict[str, tuple[[ActionContext, bool], Self]],
                 #make_payload: Optional[Callable[["ActionContext"], Payload]] = None,
                 on_overtime = Self | None,
                 remark: str =""):
        # Trigger conditions -> Fire Payload inside the payload list
        # Check transition conditions- > if filled (status change), move to next node.
        # If next node is None, switch Signal Status to Terminated. 
        # trigger_cond = 
        #transitions = {
        #    "TP": (lambda ctx: ctx.price > 105, tp_node),
        #    "SL": (lambda ctx: ctx.price < 95, sl_node)
        #    }
        self.status: ActionStatus = ActionStatus.PENDING
        self.trigger_cond = trigger_cond
        self.payloads: list[Payload] = payloads  # Each action can contain multiple Payload
        
        self.transitions = transitions
        self.on_overtime = on_overtime
        self.remark = remark
        
    def evaluate(self, ctx: dict) -> Optional["ActionNode"]:
        # Only evaluate nodes that are still pending
        if self.status != ActionStatus.PENDING:
            return None

        if self.trigger_cond(ctx):
            print(f"[ActionNode] {self.name} triggered.")
            self.status = ActionStatus.ACTIVE
            for payload in self.payloads:
                try:
                    print(payload)
                    #EP = ExecutePayload(ctx.connect, payload, ctx.account_id, 
                    #                    live_order=ctx.live_order).unload()

                    #self.action(ctx)
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
        
        # Move through Tree with Step function
        # If overtime is reached, go to the overtime_node
        # If the market conditions is met and node is pending, move to the next
        # If the node is VOID, avoid going to that node and its branches
        
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
            if nxt and nxt.status != ActionStatus.VOID:
                self.current = nxt
        