#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
# Python imports
from typing import Callable, Optional, Any, field, Self
from dataclasses import dataclass
from datetime import datetime
# Python Packages imports
import nunmpy as np
# EC_API imports
from EC_API.op_strategy.enum import ActionStatus
from EC_API.op_strategy.data_feed import DataFeed
from EC_API.payload.base import Payload, ExecutePayload
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.base import LiveOrder


class ActionContext:
    def __init__(self, 
                 start_time: datetime, 
                 end_time: datetime,
                 feeds: dict[str, DataFeed]):
        self.start_time = start_time
        self.end_time = end_time
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)}
        
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
    """
    `ActionNode` is a building block for all Operational Strategy (OpStrategy).
    
    Each `ActionNode` requires a few compulsaory attributes:
        label: The name of the `ActionNode`
        payloads: A list of `Payload` objects that contains the information of 
                  the orders for for this nodes.
        trigger_cond: A Callable function (-> bool) that is used in the evaluate 
                      method. If this condition is true, we migrate all the 
                      payloads to the execution queue or Payload Database. The 
                      function input is persumed to be an `ActionContext` object 
                      (ctx).
        transitions: A dict that contains subsequemt branching `ActionNodes`. the 
                     format is {name: (transition_condition, next_node),...}.
                     Here is an example: 
                         transitions = {
                             "TP": (lambda ctx: ctx.price > 105, tp_node),
                             "SL": (lambda ctx: ctx.price < 95, sl_node)
                             }

    Note that the trigger_cond and the transition_condition are different. 
    Trigger_cond is the condition for firing ALL the `Payloads` in the payloads 
    list, while transition_condition in the transitions dict is the condition 
    for moving the pointer of the `ActionTree` to the next node. If the user 
    desired to fire payloads immediately upon the `ActionNode` being pointed to,
    make sure to make both conditions identical.
    
    Life Cycle of a ActionNode, default status: PENDING, if all payloads 
    confirmed sent-> COMPLETED. If other sibling's nodes are COMPLTETED, 
    status->VOID.

    If next node is None, switch `OpSignal` status to TERMINATED. 
        
    """
    def __init__(self, 
                 label: str,
                 payloads: list[Payload], # Payloads of this action
                 trigger_cond: Callable[ActionContext, dict],
                 transitions: dict[str, tuple[[ActionContext, bool], Self]],
                 #make_payload: Optional[Callable[["ActionContext"], Payload]] = None,
                 #on_overtime = Self | None,
                 remark: str =""):
        self.label = label
        self.payloads = payloads if payloads else []  # Each action can contain multiple Payloads
        self.trigger_cond = trigger_cond if trigger_cond else False
        self.transitions = transitions if transitions else {}
        self.status: ActionStatus = ActionStatus.PENDING  
        
        self.payloads_states = np.array([False for _ in len(self.payloads)]) 
        self.remark = remark

    def update_status(self, DB) -> None:
        payload_status = []
        for i, payload in enumerate(self.payloads):
            # Scan DB for confirmation
            #XXXX
            
            if payload.status == PayloadStatus.FILLED or PayloadStatus.ACK:
                self.payloads_states[i] = True
                 
            elif payload.status == PayloadStatus.VOID:
                self.payloads_states[i] = False

        if all(self.payloads_states):
            self.status = ActionStatus.COMPLETED
         
    
    def evaluate(self, ctx: dict) -> Optional["ActionNode"]:
        # Only evaluate nodes that are still pending
        if self.status != ActionStatus.PENDING:
            return None
        
        # Check Trigger condition and fire Payload
        if self.trigger_cond(ctx):
            print(f"[ActionNode] {self.name} triggered.")

            for payload in self.payloads:
                try: 
                    print(payload)
                    # Insert Payload to DB
                    #EP = ExecutePayload(ctx.connect, payload, ctx.account_id, 
                    #                    live_order=ctx.live_order).unload() # Actual method to send orders
    
                except Exception as e:
                    print(f"[ActionNode] {self.name} failed: {e}")
    
        # Scan database for conifrmation and change status
        self.update_status(DB)
     
        # Move the pointer to the next node
        for label, (cond, nxt_node) in self.transitions.items():
            if cond(ctx):
                #self.status = ActionStatus.EXECUTED
                #print(f"[ActionNode] {self.name} triggered → {label}")
                # Only when all payloads are confirmed executed do we cancel all other 
                # sibilings nodes
                if self.status == ActionStatus.COMPLETED:
                    # mark other branches VOID
                    for alt_label, (_, alt_node) in self.transitions.items():
                        if alt_node is not nxt_node:
                            alt_node.status = ActionStatus.VOID
                    return nxt_node
        return None



class ActionTree:
    def __init__(self, root: ActionNode, overtime_node: ActionNode):
        self.cur = root
        self.root = root
        self.overtime_node = overtime_node # Compulsory 
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
            
        if self.cur and self.cur.status == ActionStatus.PENDING:
            nxt = self.cur.evaluate(ctx)
            if nxt and nxt.status != ActionStatus.VOID:
                self.cur = nxt
        