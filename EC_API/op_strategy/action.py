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
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# EC_API imports
from EC_API.op_strategy.enum import ActionStatus
from EC_API.op_strategy.data_feed import DataFeed
from EC_API.payload.base import Payload
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
                 payloads: list[Payload] | None, # Payloads of this action
                 trigger_cond: Callable[ActionContext, dict] | None,
                 transitions: dict[str, tuple[[ActionContext, bool], Self]] | None,
                 db_session: AsyncSession = None,
                 to_db_table: str = "",
                 scan_db_tables: list[str] = [],
                 remark: str =""):
        self.label = label
        self.payloads = payloads if payloads else []  # Each action can contain multiple Payloads
        self.trigger_cond = trigger_cond if trigger_cond else False
        self.transitions = transitions if transitions else {}
        self.status: ActionStatus = ActionStatus.PENDING  
        
        self.payloads_states = np.array([False for _ in range(len(self.payloads))]) 
        # We assume the DB we used to house the Pending Payloads are an async_seesion in
        # sql_alchemy, we might change this into a message queue in the future
        self.db_session = db_session  
        self.to_db_table = to_db_table
        self.scan_db_tables = scan_db_tables
        self.remark = remark

    async def insert_payload(self) -> None:
        # In the future we might want to change this into an event-driven msg bus
        for payload in self.payloads:
            entry = self.to_db_table(
                request_id=payload.request_id,
                account_id=payload.account_id,
                status=payload.status,
                order_request_type=payload.order_request_type,
                start_time=payload.start_time,
                end_time=payload.end_time,
                order_info=payload.order_info
            )
            #entry = self.to_db_table(**payload.dict())
            self.db_session.add(entry)
        await self.db_session.commit()
        
    async def evaluate(self, ctx: dict) -> None:
        # Only evaluate nodes that are still pending
        if self.status != ActionStatus.PENDING:
            return None
        
        # Check Trigger condition and fire Payload
        if self.trigger_cond(ctx):
            print(f"[ActionNode] {self.label} triggered.")

            for payload in self.payloads:
                await self.insert_payload(payload)
        return 
    
class GoFlatNode(ActionNode): # Untested
    """
    Special ActionNode that liquidates all positions and cancels all orders.
    Triggered manually (control app) or by global override condition.
    """

    def __init__(self,
                 label: str = "GO_FLAT",
                 db_session: Optional[AsyncSession] = None,
                 to_db_table=None,
                 remark: str = "Emergency liquidation"):
        super().__init__(
            label=label,
            payloads=[],   # Will be generated dynamically
            trigger_cond=lambda ctx: True,  # Always fires once called
            transitions={},  # Terminal node
            db_session=db_session,
            to_db_table=to_db_table,
            remark=remark
        )

    async def evaluate(self, ctx: dict) -> None:
        """
        On activation, dynamically create liquidation payloads
        based on current portfolio state (positions in ctx).
        """
        if self.status != ActionStatus.PENDING:
            return None

        print("[GoFlatNode] Emergency liquidation triggered")

        # Generate cancel+liquidate payloads from positions in ctx
        positions = ctx.get("positions", {})
        self.payloads = []
        for symbol, qty in positions.items():
            if qty != 0:
                action_type = "LIQUIDATE_LONG" if qty > 0 else "LIQUIDATE_SHORT"
                payload = Payload(
                    request_id=int(datetime.now(tz=timezone.utc)*1000),
                    account_id=ctx.get("account_id", 0),
                    cl_order_id=f"goflat-{symbol}-{datetime.now(tz=timezone.utc)}",
                    status=PayloadStatus.PENDING,
                    order_request_type=OrderRequestType.CANCEL_ORDER_REQUEST,
                    start_time=datetime.utcnow(),
                    end_time=datetime.utcnow(),
                    order_info={} #{"symbol": symbol, "qty": -qty, "action": action_type}
                )
                self.payloads.append(payload)

        # Insert liquidation payloads into DB
        if self.db_session and self.to_db_table:
            for payload in self.payloads:
                entry = self.to_db_table(
                    request_id=payload.request_id,
                    account_id=payload.account_id,
                    cl_order_id=payload.cl_order_id,
                    status=payload.status,
                    order_request_type=payload.order_request_type,
                    start_time=payload.start_time,
                    end_time=payload.end_time,
                    order_info=payload.order_info
                )
                self.db_session.add(entry)
            await self.db_session.commit()

        self.status = ActionStatus.COMPLETED
        return None
        
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
        self.cur = root
        self.root = root
        
        self.overtime_cond = overtime_cond
        self.overtime_node = overtime_node # Compulsory 

        self.finished = False
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
            self.cur = None
            self.finished = True
            return
    
        # 2. Evaluate current node
        if self.cur is None:
            self.finished = True
            return

        await self.cur.evaluate(ctx)

        # 3. Transition to next node
        for label, (cond, nxt_node) in self.cur.transitions.items():
            if cond(ctx) and self.cur.status == ActionStatus.COMPLETED:
                # Cancel siblings
                for alt_label, (_, alt_node) in self.cur.transitions.items():
                    if alt_node is not nxt_node and alt_node.status == ActionStatus.PENDING:
                        alt_node.status = ActionStatus.VOID
                self.cur = nxt_node
                if not nxt_node.transitions:
                    self.finished = True
                break
            
async def update_action_status(node: ActionNode, session: AsyncSession) -> None:
    """Update a single node from DB."""
    for i, payload in enumerate(node.payloads):

        for table in node.scan_db_tables:
            stmt = select(table).where(table.request_id == payload.request_id)
            result = await node.db_session.execute(stmt)
            row = result.scalars().first()

            if row and row.status in (PayloadStatus.FILLED, PayloadStatus.ACK):
                node.payloads_states[i] = True
                break
            
    if all(node.payloads_states):
        node.status = ActionStatus.COMPLETED



