#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:06:40 2025

@author: dexter
"""
import asyncio
from typing import AsyncIterator
import logging
# Import EC_API scripts
from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.routers import MessageRouter, StreamRouter
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.base import Monitor
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import (
    MktDataSubLevelCQG, 
    )
from EC_API.monitor.cqg.enum_mapping import (    
    MKTDATASUBLEVEL_MAP_INT2CQG
    )
from EC_API.monitor.cqg.builders import (
    build_realtime_data_request_msg,
    build_reset_tracker_request_msg
    )
from EC_API.monitor.cqg.parsers import (
    parse_market_data_subscription_statuses,
    parse_real_time_market_data
    )
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.exceptions import (
    SymbolResolutionError,
    UnsupportedLevelError,
    MonitorDataRequestError,
    MonitorTimeOutError
    )
from EC_API._typing import MarketValueType

logger = logging.getLogger(__name__)

class MonitorDataCQG(Monitor):
    def __init__(self, conn: ConnectCQG):
        # Connections
        self._conn: ConnectCQG = conn
        self._transport: TransportCQG = conn.transport
        
        # Event Loop
        self._loop = asyncio.get_running_loop()
        self.timeout = self._conn._timeout

        # symbol_registry and routers
        self._stream_router: StreamRouter = self._conn._mkt_data_stream_router
        self._msg_router: MessageRouter = self._conn._msg_router
        self._symbol_registry: SymbolRegistry = SymbolRegistry()
        
        # State Control
        self.state = self._conn.state
        
    # --- Property --- 
    @property
    def conn(self):
        return self._conn

    def rid(self) -> int:
        return self.conn.rid()
        
    # --- function calls
    async def stream(
            self, 
            symbol_name: str, 
            level: MktDataSubLevel
        ) -> AsyncIterator[MarketValueType] | None:
        
        if self.state != ConnectionState.CONNECTED_LOGON:
            logger.warning(f"stream for Symbol: {symbol_name} failed. Account not logon.")
            return 

        if not symbol_name in self._symbol_registry.sym_to_contract_ids.keys():
            metadata = await self.conn.resolve_symbol(symbol_name)
            if not metadata:
                raise SymbolResolutionError(f"Failed to resolve symbol:{symbol_name}.")
                
            self._symbol_registry.register(symbol_name, metadata)
                
        contract_id = self._symbol_registry.get_contract_ids(symbol_name)

        try:
            await self._realtime_data_request(contract_id, level)
        except MonitorDataRequestError:
            logger.warning(f"sub to market data of contract_id: {contract_id} failed.")
            return 
        
        q = self._stream_router.subscribe(contract_id)
        
        try:
            while not self._conn._stop_evt.is_set():
                try:
                    msg = await q.get()
                except asyncio.TimeoutError:
                    continue
                yield parse_real_time_market_data(msg)
            
        finally:
            try:
                await self._unsubscribe_mkt_data(contract_id)
            except MonitorDataRequestError:
                logger.warning(f"Unsubscribe contract_id: {contract_id} failed.")
                return
            finally:
                self._stream_router.unsubscribe(contract_id, q)

    
    # --- CQG function calls
    async def _realtime_data_request(
            self, 
            contract_id: int, 
            level: MktDataSubLevel | MktDataSubLevelCQG
        ) -> list[dict[str, str]]:
        # !!! Import Note: Try not to have concurrent callers for the same 
        # symbol at the same time. Message Router may fail. Space out the 
        # function calls.
        if not MKTDATASUBLEVEL_MAP_INT2CQG.get(level):
            raise MonitorDataRequestError(f"Level: {level} unsupported.")
            
        with msg_io_error_handler(
                MonitorDataRequestError,
                timeout_error = MonitorTimeOutError
            ):
            msg = build_realtime_data_request_msg(contract_id, self.rid(), level)
        
            key = ('sub', 'market_data_subscription_statuses', 'contract_id', contract_id)
            fut = self._msg_router.register_key(key)
            
            await self._transport.send(msg)  
            confirm_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            return parse_market_data_subscription_statuses(confirm_msg)
    
    async def _unsubscribe_mkt_data(
            self, 
            contract_id: int
        ) -> list[dict[str,str]]:
        with msg_io_error_handler(
                MonitorDataRequestError,
                timeout_error = MonitorTimeOutError
            ):
            msg = build_reset_tracker_request_msg(contract_id, self.rid())
        
            key = ('sub', 'market_data_subscription_statuses', 'contract_id', contract_id)
            fut = self._msg_router.register_key(key)
            await self._transport.send(msg)
            confirm_msg = await asyncio.wait_for(fut, timeout=self.timeout)
            return parse_market_data_subscription_statuses(confirm_msg)

