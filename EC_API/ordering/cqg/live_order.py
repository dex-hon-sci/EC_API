#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:01:16 2025

@author: dexter
"""
import asyncio
from typing import Any
from datetime import timezone
import logging

from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
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
from EC_API.transport.routers import MessageRouter
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.ordering.cqg.builders import (
    build_new_order_request_msg, 
    build_modify_order_request_msg,
    build_cancel_order_request_msg,
    build_activate_order_request_msg,
    build_liquidateall_order_request_msg,
    build_cancelall_order_request_msg,
    build_goflat_order_request_msg
    )
from EC_API.exceptions import (
    TradeSubscriptionMissingError,
    MissingSymbolResolutionError,
    OrderRequestError,
    MsgBuilderError
    )

logger = logging.getLogger(__name__)

class LiveOrderCQG(LiveOrder):
    # a class that control the ordering action to the exchange
    # This object is specific for CQG type request
    def __init__(self, 
                 trade_session: TradeSessionCQG,
                 symbol_name: str, 
                 request_id: int, 
                 account_id: int,
                 #sub_scope: int = SubScope.ORDERS,
                 #msg_id: int = int(random_string(length=6)), # For symbol resolutions
                 auto_unsub: bool = True,
                 timeout: int | float = 1,
                 ):
        
        # Message Routing
        self._trade_session: TradeSessionCQG = trade_session
        self._conn: ConnectCQG = self._trade_session._conn
        self._transport: TransportCQG = self._conn.transport
        
        # Event Loop
        self.timeout = self._conn._timeout
                
        # CQG-related input parameters
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id
                
    # ---
    def rid(self):
        return self._conn.rid()
    
    def check_state():
        return 
    
    # --- CQG function calls
    async def _new_order_request(
            self, 
            request_details: dict[str, Any]
        ) -> None:
        para = locals().copy()
        
        try:
            client_msg = build_new_order_request_msg(**request_details)
        except MsgBuilderError:
            raise OrderRequestError 
        
        key = ('substream','order_statuses','chain_order_id','')
        #key = ("order_statuses", request_details['request_id'])
        chain_order_id = request_details['cl_order_id']
        
        self._stream_router.subscribe(chain_order_id)
        await self._transport.send(client_msg)

    
    async def _modify_order_request(
        self, 
        request_id: int,
        request_details: dict[str, Any],
        ) -> ServerMsg:
        
        try:
            client_msg = build_modify_order_request_msg(**request_details)
        except MsgBuilderError:
            raise OrderRequestError 

        key = ('substream','order_statuses','chain_order_id','')
        #key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)

        return server_msg
    
    async def _cancel_order_request(
        self,
        request_details: dict[str, Any],
        **kwargs
        ) -> ServerMsg:
        try:
            client_msg = build_cancel_order_request_msg(**request_details)
        except MsgBuilderError:
            raise OrderRequestError 
        
        key = ('substream','order_statuses','chain_order_id','')
        #key = ("order_statuses", request_details['request_id'])
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        return server_msg

    async def _activate_order_request(
        self,
        request_details: dict[str, Any],
        ) -> ServerMsg:
        try:
            client_msg = build_activate_order_request_msg(**request_details)
        except MsgBuilderError:
            raise OrderRequestError 

        #key = ("order_statuses", request_details['request_id'])
        key = ('substream','order_statuses','chain_order_id','')
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
        try:
            client_msg = build_goflat_order_request_msg(**request_details)
        except MsgBuilderError:
            raise OrderRequestError 

        #key = ("order_statuses", request_details['request_id'])
        key = ('substream','order_statuses','chain_order_id','')
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        
        return server_msg
    
    # --- Function call ---
    async def send(
        self, 
        request_type: RequestType,
        request_details: dict,
        **kwargs
        ) -> None:

        # Get the Inputs
        symbol = request_details['symbol']
        account_id = self._trade_session._conn._account_id
        contract_id = self._trade_session.sub_mgr.get_contract_id_by_name(symbol)
        rid = self._conn.rid()
        
        # Check Symbol resolution
        if not self._trade_session.symbol_registry.has_symbol(symbol):
            raise MissingSymbolResolutionError(
                f"Symbol: {symbol} is not in the registry."
                )
            
        # Check Trade ID
        if not self._trade_session.has_orders_scope():
            raise TradeSubscriptionMissingError(
                "Trade subscription has to be done before sending order."
                )

        try: # then send
            details = {
                "account_id": account_id,
                "request_id": rid,
                "contract_id": contract_id,
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
        except OrderRequestError as e:
            logger.warning(f'{request_type} request failed.')

        return server_msg

