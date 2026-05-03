#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 05:01:41 2026

@author: dexter
"""
import asyncio
import logging
from datetime import datetime
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.transport.cqg.base import TransportCQG
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.enums import OrderStatus
from EC_API.ordering.cqg.enums import SubScopeCQG
from EC_API.ordering.enums import SubScope
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg,
    build_trade_historical_orders_request_msg
    )
from EC_API.ordering.cqg.parsers import (
    parse_trade_subscription_statuses,
    parse_trade_snapshot_completions,
    ordering_parsers
    )
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.protocol.cqg.parser_util import parse_server_msg

from EC_API.exceptions import (
    TradeSessionRequestError,
    TradeSessionTimeOutError,
    TradeSubscriptionMissingError
    )
from EC_API._typing import (
    OrderStatusType, 
    ContractMetaDataType
    )

logger = logging.getLogger(__name__)

class TradeSessionCQG:
    def __init__(
            self,
            conn: ConnectCQG,
        ):
        # Connect
        self._conn = conn
        self._transport: TransportCQG = self._conn.transport
        
        # Event Loop
        self._tracker_task: asyncio.Task | None = None
        self._stop_evt: asyncio.Event = self._conn._stop_evt
        
        # Routers
        self._stream_router = self._conn._exec_stream_router
        self._msg_router = self._conn._msg_router
                
        # Containers - Subs
        self._active_subs: dict[int, set[SubScope]] = {}
        
        # Containers - orders
        self.active_orders: set[str] = set()
        self.order_statuses: dict[str, OrderStatusType] = dict() # order_id to status
        self.order_details: dict[str, dict] = dict()

        self._account_summaries: dict[str, None] = dict()
        #self._order_futures: dict[str, asyncio.Future] = {}  # for awaiting terminal state

        # symbol registry 
        self.symbol_registry: SymbolRegistry = SymbolRegistry()

        # Settings
        self.order_statuses_TTL: int = 10 #(Time-to-live in Seconds)
        
    # --- Property --- 
    @property
    def conn(self):
        return self._conn
    
    @property
    def state(self):
        return self._conn._state_mgr.cur
    
    @property
    def timeout(self):
        return self._conn._timeout

    def rid(self) -> int:
        return self.conn.rid()
    
    # ---- Dunder meothos ---
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args) -> bool:
        await self._cleanup()
        await self._conn.__aexit__(*args)
        return False
  
    # --- Checks
    def has_orders_scope(self) -> bool:
        return any(
            SubScope.ORDERS in scopes 
            for scopes in self._active_subs.values()
            )
    
    def has_positions_scope(self) -> bool:
        return any(
            SubScope.POSITIONS in scopes 
            for scopes in self._active_subs.values()
            )
    # --- Getters
    def get_order_status(self, order_id: str) -> dict:
        return self.order_statuses.get(order_id)
    
    # --- function calls
    async def wait_for_ack(self) -> None: 
        return 
    
    async def wait_for_terminal(self, order_id: str) -> dict:
        # blocks until filled/cancelled/rejected
        ...
        return dict()
    
    # --- status tracker 
    async def _tracker_loop(self):
        TERMINAL_STATES = {
            OrderStatus.FILLED, OrderStatus.CANCELLED,
            OrderStatus.REJECTED, OrderStatus.EXPIRED
            }
        # subscribes to exec_stream_router, updates _order_state
        while not self._stop_evt.is_set():
            
            # If There are new order_id added
            for chain_order_id in self.active_orders:
                queues = self._stream_router._subs.get(chain_order_id, [])

             # Look at the order status stream (By Level) using the chain_order_id
             #self._active_subs.get()
                          
             # Check the status and see if there is any changes
             # update the trackers
          
            # check if the it is at the end state, if so, log then pop
          
          
            
    # --- CQG function calls ---
    async def resolve_symbol(self, symbol_name: str) -> ContractMetaDataType:
        
        metadatas = await self._conn.resolve_symbol(symbol_name)
        print("[stream()] metadata", metadatas)
        for metadata in metadatas:
            print('entry', symbol_name, metadata['contract_metadata'],
                  type(metadata['contract_metadata']))
            self._symbol_registry.register(
                symbol_name, 
                metadata['contract_metadata']
                )
            print("[stream()] symbol registry", 
                  self._symbol_registry.active_symbols,
                  self._symbol_registry.metatdata)

        return metadatas
    
    async def deresolve_symbol(self, symbol_name: str) -> ContractMetaDataType:
        ...

        
    async def trade_subscription_request(
            self,
            sub_id: int,
            sub_scope: SubScope | SubScopeCQG                           
        ) -> ServerMsg | None:
        
        if sub_id in self._active_subs.keys():
            logger.warning("Sub_id: {sub_id} is already in-use.")
            return
        
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
        
            # wait for three response, trade_sub_Status, snapshot, orderstatus 
            sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
            snapshot_key = ('sub', 'trade_snapshot_completions', 'subscription_id', sub_id)
            fut_sub_status = self._msg_router.register_key(sub_status_key)
            fut_snapshot = self._msg_router.register_key(snapshot_key)
            
            await self._transport.send(msg)

            sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self.timeout)
            snapshot_msg = await asyncio.wait_for(fut_snapshot, timeout=self.timeout)
            return parse_server_msg(sub_status_msg, ordering_parsers),\
                   parse_server_msg(snapshot_msg, ordering_parsers)
                   
        # Fix this later. Need to refactor the parsers to parse JSON
            #return parse_trade_subscription_statuses(sub_status_msg),\
            #       parse_trade_snapshot_completions(snapshot_msg)
    
    async def unsubscribe_trade_request(
            self, 
            sub_id: int, 
            sub_scope: SubScope | SubScopeCQG
        ) -> None:
        
        
        with msg_io_error_handler(
                TradeSessionRequestError,                               
                timeout_error = TradeSessionTimeOutError
            ):
            if sub_id not in self._active_subs.keys():
                raise TradeSubscriptionMissingError(
                    f"sub_id: {sub_id} is not in the active subscription list"
                    )

            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe = False,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
            sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
            fut_sub_status = self._msg_router.register_key(sub_status_key)
            
            await self._transport.send(msg)

            sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self.timeout)
            return parse_server_msg(sub_status_msg, ordering_parsers)

    async def request_historical_orders(
            self,
            from_date: datetime, 
            to_date: datetime
        ) ->  dict[str, str]:
        
        from_date_timestamp = from_date.timestamp()
        to_date_timestamp = to_date.timestamp()
        rid = self.rid()
        with msg_io_error_handler(
                TradeSessionRequestError,
                timeout_error = TradeSessionTimeOutError
            ):
            client_msg = build_trade_historical_orders_request_msg( 
                self._conn._account_id, 
                rid,
                from_date_timestamp,
                to_date_timestamp
                )
            key = ('info', 'information_reports:historical_orders_report', 'id', rid)
            fut = self._msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        
            return server_msg
        
    # --- Lifecycle ---
    async def _cleanup(self): pass
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
