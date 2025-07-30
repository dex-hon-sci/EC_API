#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 13:19:48 2025

@author: dexter
"""
from dataclasses import dataclass, field

from WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from WebAPI.order_2_pb2 import Order as Ord #Side, OrderType, Duration

from EC_API.ordering.enums import *
from EC_API.connect import ConnectCQG
from EC_API.msg_validation.base import CQGValidMsgCheck
import datetime
from datetime import timezone



class LiveOrder(Protocol):
    def __init__(self, 
                 connect: ConnectCQG):
        self._connect = connect
        
    def send():
        return 
    


if __name__ == "__main__":
    ## Usage example
    # logon
    # Resolve symbol (input-> symbol)
    # Trade Subscrition (get the ORDER_ID )
    # Send order
    pass