#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 12:18:58 2025

@author: dexter
"""
# Python imports
from typing import Callable, Optional, Any, Self
# Python Packages imports
from EC_API.op_strategy.action_node import (
    ActionNode, ActionContext
    )
from EC_API.op_strategy.enums import (
    ActionStatus, 
    ACTION_STATUS_LIFECYCLE
    )
from EC_API.common.data_feed import DataFeed
from EC_API.utility.state_mgr import StateMgr

    
    
class ActionTree:
    """
    `ActionTree` controls the traversal between linked `ActionNodes`.
    
    It also enforeced a special overtime node via the overtime_node attribute.
    If the time window of OpSignal has past, `ActionTree` will default to 
    execute the overtime_node. Usually, this node contains cancel_all orders or
    liquidate_all orders type of `Payload`.
    
    Once we self.finished == True, the OpSignal turn to TERMINAL.
    
    """
    def __init__(self, 
                 root: ActionNode, 
                 overtime_cond: Callable[[ActionContext], bool],
                 overtime_node: ActionNode):
        self.head_cur = root # The pointer for PENDING nodes, transition to SENT
        self.tail_cur = root # Pointer for SENT nodes, transition to VOID or COMPLETED
        self.root = root
        
        
        self.action_ctx: ActionContext = None
        self.action_mgr = None

        self.overtime_cond = overtime_cond
        self.overtime_node = overtime_node # Compulsory 
        
        self.finished = False
        
        self._state_mgr: StateMgr = StateMgr(
            ACTION_STATUS_LIFECYCLE, 
            ActionStatus.PENDING,
            ActionStatus.PENDING,
            allowed_starts = [ActionStatus.PENDING]
            )        
        # Move through Tree with Step function
        # If overtime is reached, go to the overtime_node
        # If the market conditions is met and node is pending, move to the next
        # If the node is VOID, avoid going to that node and its branches

    async def step(self, ctx: dict) -> None:
        # ctx: ActionContext
        if self.finished:
            return
        
         # 1. Check universal overtime condition
        if self.overtime_cond and self.overtime_cond(ctx):
            if self.overtime_node.status == ActionStatus.PENDING:
                print("[ActionTree] Triggering overtime exit")
                await self.overtime_node.evaluate(ctx)
            self.head_cur = None
            self.finished = True
            return
    
        # 2. Evaluate current node
        if self.head_cur is None:
            print("Reaching the end of the Tree")
            self.finished = True
            return

        #await self.head_cur.evaluate(ctx)
        ####await ActionNodeHandler(self.head_cur, self.action_mgr).evaluate(ctx)
        
        # 3. Transition to next node
        if self.head_cur.status == self.head_cur.move_status:
            for label, (cond, nxt_node) in self.head_cur.transitions.items():
                print("check"+label, cond(ctx), self.head_cur.label, self.head_cur.status, nxt_node.label)
                if cond(ctx) and self.head_cur.status == ActionStatus.SENT:
                    print(label+": Condition match")
                    # Cancel siblings
                    for alt_label, (_, alt_node) in self.head_cur.transitions.items():
                        if alt_node is not nxt_node and alt_node.status == ActionStatus.PENDING:
                            alt_node.status = ActionStatus.CANCELLED
                            
                    print("Move from: ", self.head_cur.label)
                    self.head_cur = nxt_node
                    print("To: ", nxt_node.label)
                    
                    #if not nxt_node.transitions:
                    #    print("Reaching the end of the Tree")#
                    #    self.finished = True
                    #break
            

