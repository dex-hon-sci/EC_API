#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""

from dataclasses import dataclass, field
from EC_API.connect.base import ConnectCQG
from EC_API.ordering.CQGLiveOrder import CQGLiveOrder
from EC_API.paylaod.enums import PayloadStatus
from EC_API.ordering.enums import RequestType


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
    order_request_type: RequestType = RequestType.NEW_ORDER
    start_time: str = 0 # In long text format
    end_time: str = 0 # In long text format
    order_info: dict = field(default_factory=dict)

    
    def __post_id__(self):
        # Check the order instructions based on the order type
        # import checking classes and func specific for CQG type orders
        match self.order_request_type:
            case RequestType.NEW_ORDER:
                pass
            case RequestType.MODIFY_ORDER:
                pass
            case RequestType.CANCEL_ORDER:
                pass
            case RequestType.ACRIVATE_ORDER:
                pass
            case RequestType.CANCELALL_ORDER:
                pass
            case RequestType.LIQUIDATEALL_ORDER:
                pass
            case RequestType.GOFLAT_ORDER:
                pass
        return

    
class ExecutePayload_CQG(object):
    # Execution object for CQG trade rounting connection
    def __init__(self, 
                 connect: ConnectCQG, 
                 payload: Payload,
                 request_id: int,
                 account_id: int):
        self._connect = connect 
        self._payload = payload
        self.request_id = request_id
        self.account_id = account_id
    
    def unload(self) -> None:
        """
        Sending order request base on the payload type

        """
        CLOrder = CQGLiveOrder(self._connect, 
                               symbol_name = self._payload.order_info['symbol_name'], 
                               request_id = self.request_id, 
                               account_id = self.account_id)
        CLOrder.send(request_type = self._payload.order_request_type, 
                     request_details = self._payload.order_info)

