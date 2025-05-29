#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:26:23 2025

@author: dexter

The payload module manage and check the prerequisites (Historical Data) before
sending the payload package through the ordering function to send out liveorder.

It should be independent of WebAPI provider.
"""
from enum import Enum
from dataclasses import dataclass, field
from ordering import LiveOrder

class PayloadStatus(Enum):
    PENDING = "PENDING"
    SENT = "Sent"
    VOID = "Cancelled" # When the Payload is cancelled

@dataclass
class Payload(object):
    # An object ready to send out to the trade engine
    # Only the Trade Engine can read the Payload object
    # The Payload Object should contains all the necessary information for 
    # Sending the order.
    # Payload only concern itself with whether the order is sent or not, 
    # it does not tell you the order status (filled or not)
    ID: str
    status: PayloadStatus
    order_dict: dict

