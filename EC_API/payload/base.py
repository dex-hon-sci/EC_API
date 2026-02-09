#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""
# Python imports
from datetime import timezone, datetime, timedelta
from dataclasses import dataclass, field
# EC_API imports
from EC_API.connect.base import Connect
from EC_API.ordering.base import LiveOrder
from EC_API.ordering.enums import SubScope, OrderStatus
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import PayloadFormatCheck

@dataclass
class Payload:
    """
    A vendor-agnoistic objects that contain the information needed for a 
    live order. 
    
    Payload only contains information about whether the order is sent or not,
    but not if the order has been filled or not.
    
    Upon instantiation, `Payload` objects perform a safety check for the 
    input parameters. The instantiation will fail if there are any illegal
    inputs.
    
    One Payload correspond to one order request.
    """
    account_id: int = 0
    request_id: int = 0
    status: PayloadStatus = PayloadStatus.PENDING
    order_request_type: RequestType = RequestType.NEW_ORDER
    start_time: datetime = datetime.now(timezone.utc)\
                                    + timedelta(days=1)# In long text format
    end_time: datetime = datetime.now(timezone.utc)\
                                    + timedelta(days=2) # In long text format
    order_info: dict = field(default_factory=dict)
    check_method: PayloadFormatCheck = PayloadFormatCheck
    asset_safty_range: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        check_obj = self.check_method(self.order_request_type, 
                                      self.order_info,
                                      self.asset_safty_range)
        check_obj.run()
        

class ExecutePayload:
    """
    A wrapper class for vendor-specific `LiveOrder` objects.
    
    This class is meant to route `Payload` data create `LiveOrder`-like 
    objects and perform their respective functions
    """
    # Execution object for CQG trade rounting connection
    def __init__(
            self, 
            connect: Connect, 
            payload: Payload,
            request_id: int,
            account_id: int,
            live_order: LiveOrder = LiveOrder
        ):
        self._connect = connect 
        self.payload = payload
        self.account_id = account_id
        self.live_order = live_order # LiveOrder class, changable by users.
        self.sub_scope: SubScope = SubScope.SUBSCRIPTION_SCOPE_ORDERS
        # Choose what enums are used for match cases in change payload status
        self.ordering_enums: OrderStatus = OrderStatus
        
    def unload(self) -> None:
        """
        Sending order request base on vendor-specific format and logics.

        """
        # Only send payload that is pending.
        if self._payload.status == PayloadStatus.PENDING:
            CLOrder = self.live_order(
                self._connect, 
                symbol_name = self.payload.order_info['symbol_name'], 
                request_id = self.payload.request_id, 
                account_id = self.account_id,
                sub_scope = self.sub_scope
                )
            server_msg = CLOrder.send(request_type = self.payload.order_request_type, 
                                      request_details = self.payload.order_info)
            
        else:
            raise Exception("Only pending payloads can be unloaded.")
        

    

    
