#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 14:40:16 2025

@author: dexter
"""
from typing import Callable, Optional, Any, field, Self

from EC_API.common.data_feeds import DataFeed
from EC_API.op_strategy.enums import ActionStatus 
from EC_API.utility.state_mgr import StateMgr


class ActionContext:
    """ ActionContext is in charge of the DataFeed related operation"""
    def __init__(self, 
                 feeds: dict[str, DataFeed]):
        self.feeds = feeds   # e.g. {"WTI": DataFeed(...), "Brent": DataFeed(...)}
        
        # Exchange specific attributes
        self.connect: str = ""
        self.account_id: str = ""
        
    def get_feed(self, symbol: str) -> DataFeed | None:
        return self.feeds.get(symbol)
      
    def get_stat(self, symbol: str, horizon: float, current_time: float) -> dict[str, float | None]:
        """Shortcut to fetch stats from a feed"""
        feed = self.get_feed(symbol)
        if feed:
            return feed.tick_buffer_stat(horizon, current_time)
        return {}
      
    def all_stats(self, horizon: float, current_time: float) -> dict[str, dict[str, float | None]]:
        """Return stats for ALL feeds at once"""
        return {
            symbol: feed.tick_buffer_stat(horizon, current_time)
            for symbol, feed in self.feeds.items()
            }  


class ActionNode:
    """
    `ActionNode` is a building block for all Operational Strategy (OpStrategy).
    
    Each `ActionNode` requires a few compulsaory attributes:
        label: The name of the `ActionNode`.
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
    confirmed SENT-> COMPLETED. 
    If other sibling's nodes are COMPLTETED, status->VOID.

    If next node is None, switch `OpSignal` status to TERMINATED. 
        
    """
    def __init__(self, 
                 label: str,
                 payloads: list[dict] | None, # Payloads of this action
                 trigger_cond: Callable[ActionContext, dict] | None,
                 transitions: dict[str, tuple[[ActionContext, bool], Self]] | None,
                 remark: str =""):
        # Name of the Action Node
        self.label = label
        # Each action can contain multiple Payloads
        self.payloads = payloads if payloads else []  
        self.trigger_cond = trigger_cond if trigger_cond else False
        self.transitions = transitions if transitions else {}
                
        # -------------
        self._state_mgr: StateMgr = None #StateMgr(
            #ACTION_STATUS_LIFECYCLE, 
            #ActionStatus.PENDING,
            #ActionStatus.PENDING,
            #allowed_starts = [ActionStatus.PENDING]
            #)
            
        # -------------
        self.payloads_states = [False for _ in range(10)]
        
        # Transition_rules 
        # (Once this Node reaches SENT or COMPLETED, we proceed to check transitions)
        self.move_on_sent = True
        self.move_on_complete = False
        if not (self.move_on_sent ^ self.move_on_complete): # Check Validity
            raise Exception(
                "An Action Node can either be moved on SENT or\
                COMPLETED. Set either move_on_sent or move_on_complete\
                to True."
                )
        if self.move_on_sent:
            self.move_status = ActionStatus.SENT
        if self.move_on_complete:
            self.move_status = ActionStatus.COMPLETED
        
    # --- Internals ---
    @property
    def state(self) -> ActionStatus:
        return self._state_mgr.cur

    # -----------------
    async def insert_order_info(self) -> None:
        # In the future we might want to change this into an event-driven msg bus
        ...
            
    async def evaluate(self, ctx: dict) -> None:
        # Only evaluate nodes that are still pending
        # Status: PENDING -> SENT
        if self.state != ActionStatus.PENDING:
            return None
        
        # Check Trigger condition and fire Payload
        if self.trigger_cond(ctx):
            print(f"[ActionNode] {self.label} triggered.")

            for payload in self.payloads:             
                await self.insert_payload()
                self.state = ActionStatus.SENT
        return 
    
    async def listen_for_conifrm(self) -> None:
        # Status: SENT -> COMPLETED/VOID
        if self.state != ActionStatus.SENT:
            return None
        
        for i, payload in enumerate(self.payloads):
            ...
                
        if all(self.payloads_states):
            self.state = ActionStatus.COMPLETED
            
        return 
    
class GoFlatNode(ActionNode): # Untested
    """
    Special ActionNode that liquidates all positions and cancels all orders.
    Triggered manually (control app) or by global override condition.
    """

    def __init__(self,
                 label: str = "GO_FLAT",
                 remark: str = "Emergency liquidation"):
        super().__init__(
            label=label,
            payloads=[],   # Will be generated dynamically
            trigger_cond=lambda ctx: True,  # Always fires once called
            transitions={},  # Terminal node
            remark=remark
        )

    async def evaluate(self, ctx: dict) -> None:
        """
        On activation, dynamically create liquidation payloads
        based on current portfolio state (positions in ctx).
        
        Status
        """
        if self.state != ActionStatus.PENDING:
            return None

        print("[GoFlatNode] Emergency liquidation triggered")

        # Generate cancel+liquidate payloads from positions in ctx
        positions = ctx.get("positions", {})
        self.payloads = []
        for symbol, qty in positions.items():
            if qty != 0:
                action_type = "LIQUIDATE_LONG" if qty > 0 else "LIQUIDATE_SHORT"
                payload = None
                self.payloads.append(payload)

        # Insert liquidation payloads into DB


        self.state = ActionStatus.COMPLETED
        return None
