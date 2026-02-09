#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:55:13 2025

@author: dexter

This Enum file contain the most relevant enums for ordering.
"""
# Python imports
from enum import Enum, auto

class RequestType(Enum):
    NEW_ORDER = "new_order_request"
    MODIFY_ORDER = "modify_order_request"
    CANCEL_ORDER = "cancel_order_request"
    SUSPEND_ORDER = "suspend_order_request"
    ACTIVATE_ORDER = "activate_order_request"
    CANCELALL_ORDER = "cancelall_order_request"
    LIQUIDATEALL_ORDER = "liquidateall_order_request"
    GOFLAT_ORDER = "goflat_order_request"
    
class SubScope(Enum):
    ORDERS = "Orders"
    POSITIONS = "Positions"
    ACCOUNT_SUMMARY = "Account-Summary"

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    MKT = "Market"
    LMT = "Limit"
    STP = "Stop"
    STL = "Stop-Limit"
    
class Duration(Enum):
    DAY = "Day"
    GTC = "Good-Till-Cancel"
    GTD = "Good-Till-Date"
    FOK = "Fill-Or-Kill"

class ExecInstruction(Enum):
    NONE = "None"
    AON = "All-Or-None"
    ICEBERG = "Iceberg"
    TRAIL = "Trailing"
    POSTONLY = "Post-Only"

class OrderStatus(Enum):
    # REJECTED, WORKING, CANCELLED, FILLED, EXPIRED: Big Five
    # IN_TRANSIT, IN_CANCEL, IN_MODIFY: Pending
    PENDING = auto()
    OPEN = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    PARTIAL = auto()
    ERROR = auto()