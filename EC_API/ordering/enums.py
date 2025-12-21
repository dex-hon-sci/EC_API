#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:55:13 2025

@author: dexter

This Enum file contain the most relevant enums for ordering.
"""
# Python imports
from enum import Enum, auto
# EC_API imports
#from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
#from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord #Side, OrderType, Duration

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
    #COLLATERAL = "Collateral"
    ACCOUNT_SUMMARY = "Account-Summary"
    #EXCHANGE_POSITIONS = "Exchange-Positions"
    #EXCHANGE_BALANCES = "Exchange-Positions"

class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(Enum):
    MKT = "Market"
    LMT = "Limit"
    STP = "Stop"
    STL = "Stop-Limit"
    #CROSS = "Cross"
    
class Duration(Enum):
    DAY = "Day"
    GTC = "Good-Till-Cancel"
    GTD = "Good-Till-Date"
    FOK = "Fill-Or-Kill"
    #GTT = "Good-Till-Time"
    #FAK = "Fill-And-Kill"
    #ATO = "At-The-Open"
    #ATC = "At-The-Close"
    #GFA = "Good-For-Auction"
    
class ExecInstruction(Enum):
    NONE = "None"
    AON = "All-Or-None"
    ICEBERG = "Iceberg"
    TRAIL = "Trailing"
    #FUNARI = ""
    #MIT = ""
    #MLM = ""
    POSTONLY = "Post-Only"
    #MTL = ""
    #AUCTION = ""
    #ATANYPRICE = ""
    #LMT_PRARGD = ""
    #ICO = ""

class OrderStatus(Enum):
    # REJECTED, WORKING, CANCELLED, FILLED, EXPIRED: Big Five
    # IN_TRANSIT, IN_CANCEL, IN_MODIFY: Pending
    # SUSPENDED: 
    PENDING = auto()
    OPEN = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    PARTIAL = auto()
    ERROR = auto()
    
# =============================================================================
#     IN_TRANSIT = "In-Transit"  # Original order is sent to execution system.
#     REJECTED = "Rejected"  # Order is rejected.
#     WORKING = "Working"  # Order is acknowledged by execution system and perhaps partially filled.
#     EXPIRED = "Expired"  # Order is expired.
#     IN_CANCEL = "In-Cancel"  #Cancel request is sent to execution system.
#     IN_MODIFY = "In-Modify"  # Modify request is sent to execution system.
#     CANCELLED = "Cancelled"  # Order is canceled.
#     FILLED = "Filled"  # Order is completely filled by execution system.
#     SUSPENDED = "Suspended"  # Order is waiting submission to execution system.
#     DISCONNECTED = "Disconnected"  # Order may be canceled because a disconnect occurred.
#     ACTIVEAT = "Activate"  # Order will be placed at a specified time (waiting execution system to start accepting orders).
#     APPROVE_REQUIRED = "Approved-required"  # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
#     APPROVED_BY_EXCHANGE = "Approved-by-exchange" 
#     APPROVE_REJECTED = "Approve-Rejected" 
#     MATCHED = "Matched" 
#     PARTIALLY_MATCHED = "Partially-Matched" 
#     TRADE_BROKEN = "Trade-Broken" 
# =============================================================================
