#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:01:16 2025

@author: dexter
"""
import asyncio
from typing import Any
from datetime import timezone

from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
#from EC_API.connect.hearback import hearback, get_contract_metadata
from EC_API.ordering.enums import (
    SubScope, OrderType,
    Duration, RequestType, 
    ExecInstruction, OrderStatus
    )
from EC_API.ordering.cqg.enums import (
    SubScopeCQG, OrderTypeCQG,
    DurationCQG, ExecInstructionCQG,
    OrderStatusCQG
    )
from EC_API.ordering.base import LiveOrder
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.router import MessageRouter
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg,
    build_new_order_request_msg, 
    build_modify_order_request_msg,
    build_cancel_order_request_msg,
    build_activate_order_request_msg,
    build_liquidateall_order_request_msg,
    build_cancelall_order_request_msg,
    build_goflat_order_request_msg
    )

class LiveOrderCQG(LiveOrder):
    # a class that control the ordering action to the exchange
    # This object is specific for CQG type request
    def __init__(self, 
                 conn: ConnectCQG, 
                 router: MessageRouter,
                 symbol_name: str, 
                 request_id: int, 
                 account_id: int,
                 sub_scope: int = SubScope.ORDERS,
                 #msg_id: int = int(random_string(length=6)), # For symbol resolutions
                 auto_unsub: bool = True,
                 timeout: int | float = 1,
                 ):
        
        # Message Routing
        self._conn = conn
        self._transport = self._conn.transport
        self._router = router
        
        # CQG-related input parameters
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id
        self.sub_scope = sub_scope
        #self.msg_id = msg_id
        self.trade_subscription_id = 0
        
        #self._per_order_queues = dict[]
        self._order_state: dict[str, dict] = {}          # order_id -> latest parsed state
        self._terminal_fut: dict[str, asyncio.Future] = {}  # order_id -> Future
        # Settings
        self.auto_unsub = auto_unsub
        self.timeout = timeout
        
    def rid(self):
        return self._conn.rid
    
    async def resolve_symbol(self):
        return await self._conn.resolve_symbol(self.symbol)
    
    async def _request_trade_subscription(
        self, 
        subscribe: bool = True,
        skip_orders_snapshot: bool = False,
        timeout: float = 1.0
        ) -> None:
                
        client_msg = build_trade_subscription_msg(
            trade_subscription_id=self.trade_subscription_id,
            subscribe = subscribe,
            skip_orders_snapshot = skip_orders_snapshot
            )
        #rid = 0 # < --- look up and fix
        rid = self._conn.msg_id()
        key = ("trade_subscription_statuses", rid)
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        await asyncio.wait_for(fut, timeout=timeout)
        
    async def _new_order_request(
        self, 
        request_details: dict[str, Any],
        ) -> ServerMsg:
        para = locals().copy()
        
        rid = self._conn.msg_id()
        client_msg = build_new_order_request_msg(**request_details)
        
        key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        
        #return parse_order_update(server_msg) # < -- this is the real output, build func later
        return server_msg
    
    async def _modify_order_request(
        self, 
        request_id: int,
        request_details: dict[str, Any],
        ) -> ServerMsg:
        client_msg = build_modify_order_request_msg(**request_details)
        
        key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)

        return server_msg
    
    async def _cancel_order_request(
        self,
        request_details: dict[str, Any],
        **kwargs
        ) -> ServerMsg:

        client_msg = build_cancel_order_request_msg(**request_details)
        key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        return server_msg

    async def _activate_order_request(
        self,
        request_details: dict[str, Any],
        ) -> ServerMsg:
        
        client_msg = build_activate_order_request_msg(**request_details)
        key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)

        return server_msg
 
    async def _cancel_all_oreder_request(self) -> None:
        ...
        return 
    
    async def liquidateall_order_request(self) -> None:
        ...
        return 
    
    async def goflat_order_request(
        self, 
        request_details: dict[str, Any],
        ) -> ServerMsg:
        
        client_msg = build_goflat_order_request_msg(**request_details)
        key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        
        return server_msg

    async def send_once(
        self, 
        request_type: RequestType,
        request_details: dict,
        **kwargs
        ) -> None:
        
        # resolve symbol -> get CONTRACT_ID from Contractmetadata
        #CONTRACT_METADATA = await self._resolve_symbols(msg_id = self.msg_id, subscribe=None)
        CONTRACT_METADATA = await self._conn.resolve_symbol(self._symbol_name)
        CONTRACT_ID = CONTRACT_METADATA.contract_id

        # Trade Subscription 
        CONTRACT_ID = await self._request_trade_subscription(
            self.trade_subscription_id,
            subscribe = True,
            sub_scope = self.sub_scope
            )
        # 2) ensure subscription (optional but recommended even for send_once)
        #handle = await self._subs.ensure_orders_subscribed(account_id=self.account_id, timeout=timeout)
        rid = self._conn.msg_id()

        try:
            details = {
                "account_id": self.account_id,
                "request_id": rid,
                "contract_id": CONTRACT_ID,
                **request_details,  
                }
        
            match request_type:
                case RequestType.NEW_ORDER:
                    # For new_order_request -> return OrderID
                    server_msg = await self._new_order_request(details)
                    
                case RequestType.MODIFY_ORDER:
                    # For other oder_requests, use the OrderID from new_order_request
                    server_msg = await self._modify_order_request(details)
                
                case RequestType.CANCEL_ORDER:
                    server_msg = await self._cancel_order_request(details)
                
                case RequestType.ACRIVATE_ORDER:
                    server_msg = await self._activate_order_request(details)
                
                case RequestType.CANCELALL_ORDER:
                    server_msg = await self._cancelall_order_request(details)
                    
                case RequestType.LIQUIDATEALL_ORDER:
                    server_msg = await self._liquidateall_order_request(details)
                    
                case RequestType.GOFLAT_ORDER:
                    server_msg = await self._goflat_order_request(details)
        
        finally:
            if self.auto_unsub:
                # Unsubscribe from trade subscription
                unsub_trade_msg = await self._request_trade_subscription(
                    self.trade_subscription_id,
                    subscribe = False,
                    sub_scope =self.sub_scope
                    )

        return server_msg


    async def place_order():
        # a more comprehesive send that separate subscription and send
        return 


