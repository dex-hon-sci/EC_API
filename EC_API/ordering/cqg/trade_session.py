#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 05:01:41 2026

@author: dexter
"""
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg
    )

class TradeSessionCQG:
    def __init__(
            self,
            conn: ConnectCQG,
        ):
        self._conn = conn
        self._transport = self._conn.transport
        self._stream_router = self._conn._exec_stream_router
        
    async def trade_subscription_request(self) -> None:
        msg = build_trade_subscription_msg()
        self._transport.send(msg)
        return 
    
    async def unsubscribe_trade_request() -> None:...
    
    
    async def wait_for_ack() -> None: ...
    
    #build_trade_subscription_msg(
    #    trade_subscription_id: int, 
    #    subscribe: bool,
    #    sub_scope: SubScope | SubScopeCQG,
    #    skip_orders_snapshot: bool    
    #    )