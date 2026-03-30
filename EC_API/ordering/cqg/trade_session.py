#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 05:01:41 2026

@author: dexter
"""
from EC_API.connect.cqg.base import ConnectCQG

class TradeSessionCQG:
    def __init__(
            self,
            conn: ConnectCQG,
        ):
        self.conn = conn
        
    def trade_subscription_request():...
    
    def unsubscribe_trade_request():...
    
    #build_trade_subscription_msg(
    #    trade_subscription_id: int, 
    #    subscribe: bool,
    #    sub_scope: SubScope | SubScopeCQG,
    #    skip_orders_snapshot: bool    
    #    )