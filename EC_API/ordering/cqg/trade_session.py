#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 05:01:41 2026

@author: dexter
"""
import asyncio
import logging
from datetime import datetime
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.enums import OrderStatus
from EC_API.ordering.cqg.enums import SubScopeCQG
from EC_API.ordering.enums import SubScope
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg,
    build_trade_historical_orders_request_msg
    )
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.exceptions import (
    TradeSessionRequestError,
    TradeSessionTimeOutError
    )
from EC_API._typing import OrderStatusType

logger = logging.getLogger(__name__)

class TradeSessionCQG:
    def __init__(
            self,
            conn: ConnectCQG,
        ):
        # Connect
        self._conn = conn
        self._transport = self._conn.transport
        
        # Event Loop
        self._timeout = self._conn._timeout
        self._tracker_task: asyncio.Task = None
        self._stop_evt = self._conn._stop_evt
        
        # Routers
        self._stream_router = self._conn._exec_stream_router
        self._msg_router = self._conn._msg_router
        
        # Containers
        self._active_subs: dict[int, set[SubScope]] = {}
        
        self.active_orders: set[str] = set()
        self.order_statuses: dict[str, OrderStatusType] = dict()

        self._account_summaries: dict[str, None] = dict()
        #self._order_futures: dict[str, asyncio.Future] = {}  # for awaiting terminal state

        # symbol registry 
        self.symbol_registry: SymbolRegistry = SymbolRegistry()
        
        # States control
        self.state = self._conn.state
        
    # --- Property --- 
    @property
    def conn(self):
        return self._conn

    def rid(self) -> int:
        return self.conn.rid()
    
    # ---- Dunder meothos ---
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for sub_id, scopes in list(self._active_subs.items()):
            for scope in scopes:
                try:
                    await self.unsubscribe_trade_request(sub_id, scope)
                except Exception: # <-- fix this later
                    pass
        if self._tracker_task and not self._tracker_task.done():
            self._tracker_task.cancel()
            try:
                await self._tracker_task
            except asyncio.CancelledError:
                pass
        return False        

    # --- Checks
    def has_orders_scope(self) -> bool:
        return any(SubScope.ORDERS in scopes 
                   for scopes in self._active_subs.values())
    
    def has_positions_scope(self) -> bool:
        return any(SubScope.POSITIONS in scopes 
                   for scopes in self._active_subs.values())
    # --- Getters
    def get_order_status(self, order_id: str) -> dict:
        return self._order_state.get(order_id)
    
    # --- function calls
    async def wait_for_ack(self) -> None: ...
    
    async def wait_for_terminal(self, order_id: str) -> dict:
        # blocks until filled/cancelled/rejected
        ...
    
    async def _tracker_loop(self):
        # subscribes to exec_stream_router, updates _order_state
        while not self._stop_evt.is_set():
            
             # Look at the order status stream (By Level) using the chain_order_id
             self._active_subs.get()
             # update the trackers
          
            # check if the it is at the end state, if so, pop
          
          
            
    # --- CQG function calls ---
    async def trade_subscription_request(
            self,
            sub_id: int,
            sub_scope: SubScope | SubScopeCQG                           
        ) -> None:
        
        # check symbol resolution,
        
        with msg_io_error_handler(
                TradeSessionRequestError, 
                timeout_error = TradeSessionTimeOutError
            ):
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe=True,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
        
            await self._transport.send(msg)
            # wait for three response, trade_sub_Status, snapshot, orderstatus 
            sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
            snapshot_key = ('sub', 'trade_snapshot_completions', 'subscription_id', sub_id)
            fut_sub_status = self._msg_router.register_key(sub_status_key)
            fut_snapshot = self._msg_router.register_key(snapshot_key)
            
            print(fut_sub_status)
            print(fut_snapshot)
            
            sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self._timeout)
            snapshot_msg = await asyncio.wait_for(fut_snapshot, timeout=self._timeout)
            
            return sub_status_msg, snapshot_msg
    
    async def unsubscribe_trade_request(
            self, 
            sub_id: int, 
            sub_scope: SubScope | SubScopeCQG
        ) -> None:
        with msg_io_error_handler(
                TradeSessionRequestError,                               
                timeout_error = TradeSessionTimeOutError
            ):
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe = False,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
            #except MsgBuilderError as e:
            #    raise TradeSessionRequestError(
            #        f"Failed to build unsubscribe_trade_request for sub_id:{sub_id}."
            #        ) from e
            await self._transport.send(msg)
            sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
            fut_sub_status = self._msg_router.register_key(sub_status_key)
            sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self._timeout)
            return sub_status_msg

    async def request_historical_orders(
            self,
            from_date: datetime, 
            to_date: datetime
        ) ->  dict[str, str]:
        
        #from_date_timestamp = from_date.timestamp()
        #to_date_timestamp = to_date.timestamp()
        rid = self.rid
        with msg_io_error_handler(
                TradeSessionRequestError,
                timeout_error = TradeSessionTimeOutError
            ):
            client_msg = build_trade_historical_orders_request_msg( 
                self._conn.account_id, 
                rid,
                from_date,
                to_date
                )
            #except MsgBuilderError as e:
            #    raise TradeSessionRequestError(
            #        f"Failed to build request_historical_orders for time period:{from_date} to {to_date}."
            #        ) from e
            key = ('info', 'information_reports:historical_orders_report', 'id', rid)
            fut = self._router.register(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self._timeout)
        
            return server_msg
        
# =============================================================================
#         
# ---
#   Proposed Structure
# 
#   Two containers, exactly as you described:
# 
#   # in TradeSessionCQG.__init__
# 
#   self._active_orders: set[str]              = set()
#   # chain_order_id → latest parsed status dict
#   self._order_state:   dict[str, dict]       = {}
# 
#   The _order_futures dict you've already commented out can stay out — the one-shot
#   msg_router Future handles the initial ack, these two are purely for the tracker loop.
# 
#   ---
#   _tracker_loop Logic
# 
#   The key insight is that stream_router is keyed by chain_order_id. Each active order
#   has its own queue. The loop just drains all active queues non-blockingly each
#   iteration:
# 
#   TERMINAL = {OrderStatus.FILLED, OrderStatus.CANCELLED,
#               OrderStatus.REJECTED, OrderStatus.EXPIRED}
# 
#   async def _tracker_loop(self):
#       while not self._stop_evt.is_set():
#           done = set()
# 
#           for chain_order_id in self._active_orders:
#               queues = self._stream_router._subs.get(chain_order_id, [])
#               for q in queues:
#                   while not q.empty():
#                       order_status_msg = q.get_nowait()
#                       status = parse_order_status(order_status_msg)  # your parser
#                       self._order_state[chain_order_id] = status
# 
#                       if status['status'] in TERMINAL:
#                           done.add(chain_order_id)
# 
#           for chain_order_id in done:
#               self._active_orders.discard(chain_order_id)
#               # optionally unsubscribe the queue here too
# 
#           await asyncio.sleep(0)   # yield to event loop, keeps it lightweight
# 
#   asyncio.sleep(0) instead of a timed sleep — it yields control back to the event loop
#   every cycle without adding artificial latency. The loop only does real work when
#   queues are non-empty.
# =============================================================================
