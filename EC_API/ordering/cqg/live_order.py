#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:01:16 2025

@author: dexter
"""
import asyncio
from typing import Any
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
from EC_API.transport.routers import MessageRouter, StreamRouter
from EC_API.ordering.cqg.trade_session import TradeSessionCQG
from EC_API.ordering.cqg.enum_mapping import OrderStatus_MAP_CQG2INT
from EC_API.ordering.cqg.builders import (
    build_new_order_request_msg, 
    build_modify_order_request_msg,
    build_cancel_order_request_msg,
    build_activate_order_request_msg,
    build_liquidateall_order_request_msg,
    build_cancelall_order_request_msg,
    build_goflat_order_request_msg
    )
from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.exceptions import (
    TradeSubscriptionMissingError,
    MissingSymbolResolutionError,
    OrderRequestError,
    LiveOrderTimeOutError,
    MissingOrderIDError
    )

logger = logging.getLogger(__name__)

class LiveOrderCQG(LiveOrder):
    # a class that control the ordering action to the exchange
    # This object is specific for CQG type request
    def __init__(
            self, 
            trade_session: TradeSessionCQG,
            symbol_name: str, 
            request_id: int, 
            account_id: int,
            timeout: int | float = 1,
        ):                 #sub_scope: int = SubScope.ORDERS,
                 #auto_unsub: bool = True,

        # Message Routing
        self._trade_session: TradeSessionCQG = trade_session
        self._conn: ConnectCQG = self._trade_session._conn
        self._transport: TransportCQG = self._conn.transport
        
        self.msg_router: MessageRouter = self._conn._msg_router
        self.stream_router: StreamRouter = self._conn._exec_stream_router
                        
        # CQG-related input parameters
        self._symbol_name = symbol_name
        self.request_id = request_id
        self.account_id = account_id
                
    # ---
    @property
    def timeout(self):
        return self._conn._timeout
    
    def rid(self):
        return self._conn.rid()
    
    def check_state(self):
        return 
    
    # --- CQG function calls
    async def _new_order_request(
            self, 
            request_details: dict[str, Any]
        ) -> ServerMsg:
        
        with msg_io_error_handler(
                OrderRequestError,
                timeout_error = LiveOrderTimeOutError
            ):
            client_msg = build_new_order_request_msg(**request_details)
            cl_order_id = request_details['cl_order_id']
            key = ('substream','order_statuses','cl_order_id', cl_order_id)
            #key = ("order_statuses", request_details['request_id'])
            fut = self.msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            
            # update trade session trackers for order's initial state 
            self._trade_session.active_orders.add(server_msg.order_statuses[0].chain_order_id)
            self._trade_session.order_statuses[server_msg.chain_order_id] = OrderStatus_MAP_CQG2INT[server_msg.result_code]
            return server_msg
    
    async def _modify_order_request(
        self, 
        request_details: dict[str, Any],
        ) -> ServerMsg:
        # check if there is a chain_order_id in the chamber
        
        with msg_io_error_handler(
                OrderRequestError,
                timeout_error = LiveOrderTimeOutError
            ):
            client_msg = build_modify_order_request_msg(**request_details)

            key = ('substream','order_statuses','chain_order_id','')
            #key = ("order_statuses", request_details['request_id'])
            fut = self.msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
    
            return server_msg
    
    async def _cancel_order_request(
        self,
        request_details: dict[str, Any],
        **kwargs
        ) -> ServerMsg:
        with msg_io_error_handler(
                OrderRequestError,
                timeout_error = LiveOrderTimeOutError
            ):
            client_msg = build_cancel_order_request_msg(**request_details)
        
            key = ('substream','order_statuses','chain_order_id','')
            #key = ("order_statuses", request_details['request_id'])
            fut = self.msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            return server_msg

    async def _activate_order_request(
        self,
        request_details: dict[str, Any],
        ) -> ServerMsg:
        with msg_io_error_handler(
                OrderRequestError,
                timeout_error = LiveOrderTimeOutError
            ):
            client_msg = build_activate_order_request_msg(**request_details)

            #key = ("order_statuses", request_details['request_id'])
            key = ('substream','order_statuses','chain_order_id','')
            fut = self.msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            return server_msg
 
    async def _cancel_all_oreder_request(self) -> ServerMsg:
        ...
        return ServerMsg()
    
    async def _liquidateall_order_request(self) -> ServerMsg:
        ...
        return ServerMsg()
    
    async def _goflat_order_request(
        self, 
        request_details: dict[str, Any],
        ) -> ServerMsg:
        with msg_io_error_handler(
                OrderRequestError,
                timeout_error = LiveOrderTimeOutError
            ):
            client_msg = build_goflat_order_request_msg(**request_details)

            #key = ("order_statuses", request_details['request_id'])
            key = ('substream','order_statuses','chain_order_id','')
            fut = self.msg_router.register_key(key)
            await self._transport.send(client_msg)
            server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            return server_msg
    
    # --- Function call ---
    async def send(
        self, 
        request_type: RequestType,
        request_details: dict,
        **kwargs
        ) -> tuple[int, asyncio.Queue] | None:

        # Get the Inputs
        symbol = request_details['symbol']
        account_id = self._trade_session._conn._account_id
        contract_id = self._trade_session.symbol_registry.get_contract_ids(symbol)
        rid = self._conn.rid()
        # Check State
        
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
            
        if request_type not in (
                RequestType.NEW_ORDER, 
                RequestType.CANCELALL_ORDER,
                RequestType.LIQUIDATEALL_ORDER,
                RequestType.GOFLAT_ORDER):
            
            order_id = request_details['order_id']
            
            if order_id not in self._trade_session.active_orders:
                raise MissingOrderIDError(
                    f"Order ID: {order_id} is not in active orders."
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
                
                case RequestType.ACTIVATE_ORDER:
                    server_msg = await self._activate_order_request(details)
                
                case RequestType.CANCELALL_ORDER:
                    server_msg = await self._cancel_all_order_request(details)
                    
                case RequestType.LIQUIDATEALL_ORDER:
                    server_msg = await self._liquidateall_order_request(details)
                    
                case RequestType.GOFLAT_ORDER:
                    server_msg = await self._goflat_order_request(details)
                    
            chain_order_id = server_msg.order_statuses[0].chain_order_id
            q = self.stream_router.subscribe(chain_order_id)

            return server_msg, q

        except OrderRequestError:
            logger.warning(f'{request_type} request failed.')
            return 


# =============================================================================
#       rid = self.rid()
#   reject_fut = self._msg_router.register_key(('rpc_reqid', 'order_request_rejects',
#   'request_id', rid))
#   ack_fut    = self._msg_router.register_key(('rpc_reqid', 'order_request_acks',
#   'request_id', rid))
# 
#   await self._transport.send(order_msg)
# 
#   done, pending = await asyncio.wait(
#       [reject_fut, ack_fut],
#       timeout=self._timeout,
#       return_when=asyncio.FIRST_COMPLETED
#   )
# 
#   for f in pending:
#       f.cancel()  # _cleanup fires, removes key from pending automatically
# 
#   if not done:
#       raise ConnectTimeOutError(...)
# 
#   result_msg = done.pop().result()
#   # inspect result_msg — is it an ACK or REJECT?
# =============================================================================
