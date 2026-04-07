#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:16:24 2026

@author: dexter
"""
import asyncio
from EC_API.connect.cqg.symbol_registry import SymbolRegistryCQG
from EC_API.monitor.cqg.realtime_data import MonitorDataCQG
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG
from EC_API.monitor.cqg.enum_mapping import MKTDATASUBLEVEL_MAP_INT2CQG
from EC_API.utility.sub_mgr import SubMgr

class DataSubMgrCQG(SubMgr):
    # enforce one subscription per contract id
    def __init__(
            self,
            session: MonitorDataCQG, 
            registry):
        self.session = session  
        
        self._conn = self.session.conn
        self.symbol_registry = SymbolRegistryCQG(self._conn)
        
    async def realtime_data_request(
        self, 
        symbol_name: str, 
        level: MktDataSubLevel | MktDataSubLevelCQG):
        # resolve symbol
        ref, fut = dict(), None
        contract_id = ref[symbol_name]
        if not MKTDATASUBLEVEL_MAP_INT2CQG.get(level):
            raise 
        try:
            LEVEL = MKTDATASUBLEVEL_MAP_INT2CQG[level]
            msg = build_realtime_data_request_msg(contract_id, self.rid(), LEVEL)
        except MsgBuilderError as e:
            return 
        q = await self._stream_router.subscribe(contract_id)

        self._transport.send(msg)
        
        # Response handling
        server_msg = await asyncio.wait_for(fut, timeout = self._timeout)
        return q
    
    async def unsubscribe_mkt_data(self, symbol_name) -> None:
        contract_id = self.sub_mgr.subs[symbol_name]
        try:
            msg = build_reset_tracker_request_msg(contract_id, self.rid())
        except MsgBuilderError as e:
            return 
        
        self._transport.send(msg)
        self._stream_router.unsubscribe(contract_id)