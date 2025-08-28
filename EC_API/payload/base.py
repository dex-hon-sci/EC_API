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
from EC_API.ordering.enums import SubScope
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import PayloadFormatCheck

@dataclass
class Payload:
    # An object ready to send out to the trade engine
    # Only the Trade Engine can read the Payload object
    # The Payload Object should contains all the necessary information for 
    # Sending the order.
    # Payload only concern itself with whether the order is sent or not, 
    # it does not tell you the order status (filled or not)
    # Payload check the format coming from Signals
    # One Payload is suppose to be one order request 
    # (New, modify, cancel, activate, cancelall,liquateall, goflat)
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
    
    def __post_init__(self) -> None:
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        #check_obj = self.check_method(self.order_request_type, 
        #                              self.order_info)
        check_obj = self.check_method(self.order_request_type, 
                                      self.order_info)
        check_obj.run()
        

class ExecutePayload:
    # Execution object for CQG trade rounting connection
    def __init__(self, 
                 connect: Connect, 
                 payload: Payload,
                 request_id: int,
                 account_id: int,
                 live_order: LiveOrder = LiveOrder):
        self._connect = connect 
        self._payload = payload
        self.account_id = account_id
        self.live_order = live_order # LiveOrder class, changable by users.
        self.sub_scope: SubScope = SubScope.SUBSCRIPTION_SCOPE_ORDERS
        
    def change_payload_status(self, server_msg) -> None:
        
        match server_msg.status:
            case "Accepted":
                self._payload.status = PayloadStatus.SENT
            case "Filled":
                self._payload.status = PayloadStatus.FILLED
                # After Filled, add Order_ID to self.order_info
            case "cancelled":
                self._payload.status = PayloadStatus.VOID
            case _:
                self._payload.status = PayloadStatus.ARCHIVED
    
    def unload(self) -> None:
        """
        Sending order request base on the payload type

        """
        # Only send payload that is pending.
        if self._payload.status == PayloadStatus.PENDING:
            CLOrder = self.live_order(self._connect, 
                                      symbol_name = self._payload.order_info['symbol_name'], 
                                      request_id = self._payload.request_id, 
                                      account_id = self.account_id,
                                      sub_scope = self.sub_scope)
            server_msg = CLOrder.send(request_type = self._payload.order_request_type, 
                                      request_details = self._payload.order_info)

            self.change_payload_status(server_msg)
            
        else:
            raise Exception("Only pending payloads can be unloaded.")
