#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:55:13 2025

@author: dexter

This Enum file contain the CQG specific enums type for ordering.

"""
# Python imports
from enum import Enum, auto
    
class SubScopeCQG(Enum):
    COLLATERAL = auto()
    EXCHANGE_POSITIONS = auto()
    EXCHANGE_BALANCES = auto()

class OrderTypeCQG(Enum):
    CROSS = auto()
    
class DurationCQG(Enum):
    GTT = auto()
    FAK = auto()
    ATO = auto()
    ATC = auto()
    GFA = auto()

class ExecInstructionCQG(Enum):
    FUNARI = auto()
    MIT = auto()
    MLM = auto()
    MTL = auto()
    AUCTION = auto()
    ATANYPRICE = auto()
    LMT_PRARGD = auto()
    ICO = auto()

class OrderStatusCQG(Enum):
    # Define Order statuses
    IN_TRANSIT = auto() #= OrderStatus.Status.IN_TRANSIT  # Original order is sent to execution system.
    REJECTED = auto() #OrderStatus.Status.REJECTED # Order is rejected.
    WORKING = auto()#OrderStatus.Status.WORKING # Order is acknowledged by execution system and perhaps partially filled.
    EXPIRED = auto() #OrderStatus.Status.EXPIRED # Order is expired.
    IN_CANCEL = auto()#OrderStatus.Status.IN_CANCEL #Cancel request is sent to execution system.
    IN_MODIFY = auto()#OrderStatus.Status.IN_MODIFY # Modify request is sent to execution system.
    CANCELLED = auto()#OrderStatus.Status.CANCELLED # Order is canceled.
    FILLED = auto() #OrderStatus.Status.FILLED # Order is completely filled by execution system.
    SUSPENDED = auto() #OrderStatus.Status.SUSPENDED # Order is waiting submission to execution system.
    DISCONNECTED = auto() #OrderStatus.Status.DISCONNECTED # Order may be canceled because a disconnect occurred.
    ACTIVEAT = auto() #OrderStatus.Status.ACTIVEAT # Order will be placed at a specified time (waiting execution system to start accepting orders).
    APPROVE_REQUIRED = auto() #OrderStatus.Status.APPROVE_REQUIRED # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
    APPROVED_BY_EXCHANGE = auto() #OrderStatus.Status.APPROVED_BY_EXCHANGE
    APPROVE_REJECTED = auto() #OrderStatus.Status.APPROVE_REJECTED
    MATCHED = auto() #OrderStatus.Status.MATCHED
    PARTIALLY_MATCHED = auto() #OrderStatus.Status.PARTIALLY_MATCHED
    TRADE_BROKEN = auto()# OrderStatus.Status.TRADE_BROKEN