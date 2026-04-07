#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 15:37:09 2026

@author: dexter
"""
import asyncio
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.enums import SubScope
from EC_API.ordering.cqg.enums import SubScopeCQG
from EC_API.ordering.cqg.builders import build_trade_subscription_msg
from EC_API.connect.cqg.symbol_registry import SymbolRegistryCQG
from EC_API.utility.sub_mgr import SubMgr
from EC_API.exceptions import MsgBuilderError

class TradeSubMgrCQG(SubMgr):
    def __init__(self, conn: ConnectCQG):
        self._pending: dict = dict()
        self._orders: dict = dict()
        
        self._symbol_registry = SymbolRegistryCQG()
        
    async def ensure_trade_subs(self, symbol_name: str) -> bool:
        # A function that ensure trade subscriptions is present 
        if symbol_name not in self._active_symbols:
            
            return False
        
        return True
            
    async def trade_subscription_request(
            self,
            sub_id: int,
            sub_scope: SubScope | SubScopeCQG                           
        ) -> None:
        try:
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe=True,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
        except MsgBuilderError:
            return 
        
        self._transport.send(msg)
        # wait for three response, trade_sub_Status, snapshot, orderstatus 
        sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
        snapshot_key = ('sub', 'trade_snapshot_completions', 'subscription_id', 1)
        fut_sub_status = self._msg_router.register_key(sub_status_key)
        fut_snapshot = self._msg_router.register_key(snapshot_key)
        
        sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self._timeout)
        snapshot_msg = await asyncio.wait_for(fut_snapshot, timeout=self._timeout)
        
        return 
    
    async def unsubscribe_trade_request(self, sub_id, sub_scope) -> None:
        try:
            msg = build_trade_subscription_msg(
                sub_id, 
                subscribe = False,
                sub_scope = sub_scope,
                skip_orders_snapshot = False   
                )
        except MsgBuilderError:
            return 
        self._transport.send(msg)
        sub_status_key = ('sub', 'trade_subscription_statuses', 'id', sub_id)
        fut_sub_status = self._msg_router.register_key(sub_status_key)
        sub_status_msg = await asyncio.wait_for(fut_sub_status, timeout=self._timeout)
        return 