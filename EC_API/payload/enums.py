#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:27:33 2025

@author: dexter
"""

from enum import Enum

class PayloadStatus(Enum):
    PENDING = "Pending"
    SENT = "Sent"
    VOID = "Cancelled" # When the Payload is cancelled
    
class OrderRequestType(Enum):
    # Order types in the CQG ordering format
    NEW_ORDER_REQUEST = "New_order_request"
    MODIFY_ORDER_REQUEST = "Modify_order_request"
    CANCEL_ORDER_REQUEST = "Cancel_order_request"
    GOFLAT_ORDER_REQUEST = "GoFlat_order_request"