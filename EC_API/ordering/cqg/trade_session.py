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
from EC_API.ordering.cqg.sub_mgr import TradeSubMgrCQG
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg,
    build_trade_historical_orders_request_msg
    )
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.exceptions import (
    MsgBuilderError
    )

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
        
        # Routers
        self._stream_router = self._conn._exec_stream_router
        self._msg_router = self._conn._msg_router
        
        # States control
        self._active_subs: dict[int, set[SubScope]] = {}
        self.order_statuses: dict[str, OrderStatus] = dict()
        self._order_state: dict[str, dict] = {}        # order_id → latest status
        self._order_futures: dict[str, asyncio.Future] = {}  # for awaiting terminal state
        self._tracker_task: asyncio.Task = None

        # symbol registry and Subscirption Manager
        self.symbol_registry: SymbolRegistry = SymbolRegistry()
        self.sub_mgr: TradeSubMgrCQG = TradeSubMgrCQG(self.symbol_registry)
        
    # --- Property --- 
    @property
    def conn(self):
        return self._conn

    def rid(self) -> int:
        return self.conn.rid()
        

    # --- Checks
    def has_orders_scope(self) -> bool:
        return any(SubScope.ORDERS in scopes 
                   for scopes in self._active_subs.values())
        
    # --- function calls
    async def wait_for_ack(self) -> None: ...
    
    async def _tracking_loop(self):
      # subscribes to exec_stream_router, updates _order_state
      while True:
          ...

    def get_order_status(self, order_id: str) -> dict:
        return self._order_state.get(order_id)
    
    async def wait_for_terminal(self, order_id: str) -> dict:
        # blocks until filled/cancelled/rejected
        ...
            
    # --- CQG function calls ---
    async def trade_subscription_request(
            self,
            sub_id: int,
            sub_scope: SubScope | SubScopeCQG                           
        ) -> None:
        
        # check symbol resolution,
        
        try:
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe=True,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
        except MsgBuilderError:
            return 
        
        await self._transport.send(msg)
        # wait for three response, trade_sub_Status, snapshot, orderstatus 
        sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
        snapshot_key = ('sub', 'trade_snapshot_completions', 'subscription_id', 1)
        fut_sub_status = self._msg_router.register_key(sub_status_key)
        fut_snapshot = self._msg_router.register_key(snapshot_key)
        
        sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self._timeout)
        snapshot_msg = await asyncio.wait_for(fut_snapshot, timeout=self._timeout)
        
        return sub_status_msg, snapshot_msg
    
    async def unsubscribe_trade_request(
            self, 
            sub_id: int, 
            sub_scope: SubScope | SubScopeCQG
        ) -> None:
        try:
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe = False,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
        except MsgBuilderError:
            return 
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
        try:
            client_msg = build_trade_historical_orders_request_msg( 
                self._conn.account_id, 
                rid,
                from_date,
                to_date
                )
        except MsgBuilderError:
            return 
        key = ('info', 'information_reports:historical_orders_report', 'id', rid)
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self._timeout)
        
        #return server_msg