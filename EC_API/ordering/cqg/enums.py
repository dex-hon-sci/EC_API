#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:55:13 2025

@author: dexter

This Enum file contain the CQG specific enums type for ordering.

"""
# Python imports
from enum import Enum, auto
# EC_API imports
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord #Side, OrderType, Duration
from EC_API.ext.common.shared_1_pb2 import OrderStatus
    
class SubScopeCQG(Enum):
    #SUBSCRIPTION_SCOPE_ORDERS = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS
    #SUBSCRIPTION_SCOPE_POSITIONS = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS
    COLLATERAL = auto()
    #SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY
    POSITIONS = auto()
    BALANCES = auto()

#class Side(Enum):
#    BUY = "BUY"
#    SELL = "SELL"

class OrderTypeCQG(Enum):
    CROSS = "Cross"
    
    
class DurationCQG(Enum):
    #DURATION_DAY = auto()
    #DURATION_GTC = auto()
    #DURATION_GTD = auto()
    #DURATION_FOK = auto()
    DURATION_GTT = auto()
    DURATION_FAK = auto()
    DURATION_ATO = auto()
    DURATION_ATC = auto()
    DURATION_GFA = auto()

class ExecInstructionCQG(Enum):
    #EXEC_INSTRUCTION_NONE = Ord.ExecInstruction.EXEC_INSTRUCTION_NONE
    #EXEC_INSTRUCTION_AON = Ord.ExecInstruction.EXEC_INSTRUCTION_AON
    #EXEC_INSTRUCTION_ICEBERG = Ord.ExecInstruction.EXEC_INSTRUCTION_ICEBERG
    #EXEC_INSTRUCTION_TRAIL = Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL
    FUNARI = auto()
    MIT = auto()
    MLM = auto()
    #EXEC_INSTRUCTION_POSTONLY = Ord.ExecInstruction.EXEC_INSTRUCTION_POSTONLY
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