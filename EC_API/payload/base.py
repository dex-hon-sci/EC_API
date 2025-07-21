#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""

from EC_API.ordering import LiveOrder
from .enums import PayloadStatus, OrderRequestType
from dataclasses import dataclass, field


@dataclass
class Payload(object):
    # An object ready to send out to the trade engine
    # Only the Trade Engine can read the Payload object
    # The Payload Object should contains all the necessary information for 
    # Sending the order.
    # Payload only concern itself with whether the order is sent or not, 
    # it does not tell you the order status (filled or not)
    # Payload check the format coming from Signals
    # One Payload is suppose to be one order request (New, modify, cancel, goflat)
    request_id: int = 0
    account_id: int = 0
    cl_order_id: str = ""
    status: PayloadStatus = PayloadStatus.PENDING
    order_request_type: OrderRequestType = OrderRequestType.NEW_ORDER_REQUEST
    start_time: str = 0 # In long text format
    end_time: str = 0 # In long text format
    order_info: dict = field(default_factory=dict)

    
    def __post_id__(self):
        # Check the order instructions
        
        match self.order_request_type:
            case OrderRequestType.NEW_ORDER_REQUEST:
                # For new_order_request, check for necessary inputs
                pass
            case OrderRequestType.MODIFY_ORDER_REQUEST:
                pass
            case OrderRequestType.CANCEL_ORDER_REQUEST:
                pass
            case OrderRequestType.GOFLAT_ORDER_REQUEST:
                pass
        return

    
class ExecutePayload():
    def __init__(self, payload: Payload):
        self.payload =  payload
    
    def unload(self):
        match self.order_request_type:
            case OrderRequestType.NEW_ORDER_REQUEST:
                LiveOrder().new_order_request()
            case OrderRequestType.MODIFY_ORDER_REQUEST:
                LiveOrder().modify_order_request()
            case OrderRequestType.CANCEL_ORDER_REQUEST:
                LiveOrder().cancel_order_request()
            case OrderRequestType.GOFLAT_ORDER_REQUEST:
                pass
        
        # Sending order request base on the payload type
        return 
    
    
    
# Request_id
# account_id

# cl_order_id: str
#order_id # provided by exchanges
