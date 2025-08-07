#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:37:54 2025

@author: dexter
"""

from dataclasses import dataclass, field
from EC_API.ordering.base import LiveOrder
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
    order_request_type: RequestType = RequestType.NEW_ORDER_REQUEST
    start_time: str = 0 # In long text format
    end_time: str = 0 # In long text format
    order_info: dict = field(default_factory=dict)

    
    def __post_id__(self):
        # Check the order instructions based on the order type
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

    
class ExecutePayload_CQG():
    def __init__(self, payload: Payload):
        self.payload = payload
    
    def unload(self):
        # Use the native function LiveOrder(...).send(...) instead
# =============================================================================
#         match self.order_request_type:
#             case RequestType.NEW_ORDER:
#                 LiveOrder().new_order_request()
#             case RequestType.MODIFY_ORDER:
#                 LiveOrder().modify_order_request()
#             case RequestType.CANCEL_ORDER:
#                 LiveOrder().cancel_order()
#             case RequestType.GOFLAT_ORDER_REQUEST:
#                 pass
# =============================================================================
        
        # Sending order request base on the payload type
        return 
