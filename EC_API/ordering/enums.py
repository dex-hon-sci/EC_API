#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 17:55:13 2025

@author: dexter

This Enum file contain the most relevant enums for ordering.
"""
from enum import Enum

from EC_API.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from EC_API.WebAPI.order_2_pb2 import Order as Ord #Side, OrderType, Duration
from EC_API.common.shared_1_pb2 import OrderStatus



class RequestType(Enum):
    NEW_ORDER = "new_order_request"
    MODIFY_ORDER = "modify_order_request"
    CANCEL_ORDER = "cancel_order_request"
    ACRIVATE_ORDER = "activate_order_request"
    CANCELALL_ORDER = "cancelall_order_request"
    LIQUIDATEALL_ORDER = "liquidateall_order_request"
    GOFLAT_ORDER = "goflat_order_request"
    
    
SUBSCRIPTION_SCOPE_ORDERS = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS
SUBSCRIPTION_SCOPE_POSITIONS = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS
SUBSCRIPTION_SCOPE_COLLATERAL = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_COLLATERAL
SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY
SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS
SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES = TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES

SIDE_BUY = Ord.Side.SIDE_BUY
SIDE_SELL = Ord.Side.SIDE_SELL

ORDER_TYPE_MKT = Ord.OrderType.ORDER_TYPE_MKT
ORDER_TYPE_LMT = Ord.OrderType.ORDER_TYPE_LMT
ORDER_TYPE_STP = Ord.OrderType.ORDER_TYPE_STP
ORDER_TYPE_STL = Ord.OrderType.ORDER_TYPE_STL
ORDER_TYPE_CROSS = Ord.OrderType.ORDER_TYPE_CROSS

DURATION_DAY = Ord.Duration.DURATION_DAY
DURATION_GTC = Ord.Duration.DURATION_GTC
DURATION_GTD = Ord.Duration.DURATION_GTD
DURATION_GTT = Ord.Duration.DURATION_GTT
DURATION_FOK = Ord.Duration.DURATION_FOK
DURATION_FAK = Ord.Duration.DURATION_FAK
DURATION_FOK = Ord.Duration.DURATION_FOK
DURATION_ATO = Ord.Duration.DURATION_ATO
DURATION_ATC = Ord.Duration.DURATION_ATC
DURATION_GFA = Ord.Duration.DURATION_GFA

EXEC_INSTRUCTION_NONE = Ord.ExecInstruction.EXEC_INSTRUCTION_NONE
EXEC_INSTRUCTION_AON = Ord.ExecInstruction.EXEC_INSTRUCTION_AON
EXEC_INSTRUCTION_ICEBERG = Ord.ExecInstruction.EXEC_INSTRUCTION_ICEBERG
EXEC_INSTRUCTION_TRAIL = Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL
EXEC_INSTRUCTION_FUNARI = Ord.ExecInstruction.EXEC_INSTRUCTION_FUNARI
EXEC_INSTRUCTION_MIT = Ord.ExecInstruction.EXEC_INSTRUCTION_MIT
EXEC_INSTRUCTION_MLM = Ord.ExecInstruction.EXEC_INSTRUCTION_MLM
EXEC_INSTRUCTION_POSTONLY = Ord.ExecInstruction.EXEC_INSTRUCTION_POSTONLY
EXEC_INSTRUCTION_MTL = Ord.ExecInstruction.EXEC_INSTRUCTION_MTL
EXEC_INSTRUCTION_AUCTION = Ord.ExecInstruction.EXEC_INSTRUCTION_AUCTION
EXEC_INSTRUCTION_ATANYPRICE = Ord.ExecInstruction.EXEC_INSTRUCTION_ATANYPRICE
EXEC_INSTRUCTION_LMT_PRARGD = Ord.ExecInstruction.EXEC_INSTRUCTION_LMT_PRARGD
EXEC_INSTRUCTION_ICO = Ord.ExecInstruction.EXEC_INSTRUCTION_ICO

# Define Order statuses
IN_TRANSIT = OrderStatus.Status.IN_TRANSIT  # Original order is sent to execution system.
REJECTED = OrderStatus.Status.REJECTED # Order is rejected.
WORKING = OrderStatus.Status.WORKING # Order is acknowledged by execution system and perhaps partially filled.
EXPIRED = OrderStatus.Status.EXPIRED # Order is expired.
IN_CANCEL = OrderStatus.Status.IN_CANCEL #Cancel request is sent to execution system.
IN_MODIFY = OrderStatus.Status.IN_MODIFY # Modify request is sent to execution system.
CANCELLED = OrderStatus.Status.CANCELLED # Order is canceled.
FILLED = OrderStatus.Status.FILLED # Order is completely filled by execution system.
SUSPENDED = OrderStatus.Status.SUSPENDED # Order is waiting submission to execution system.
DISCONNECTED = OrderStatus.Status.DISCONNECTED # Order may be canceled because a disconnect occurred.
ACTIVEAT = OrderStatus.Status.ACTIVEAT # Order will be placed at a specified time (waiting execution system to start accepting orders).
APPROVE_REQUIRED = OrderStatus.Status.APPROVE_REQUIRED # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
APPROVED_BY_EXCHANGE = OrderStatus.Status.APPROVED_BY_EXCHANGE
APPROVE_REJECTED = OrderStatus.Status.APPROVE_REJECTED
MATCHED = OrderStatus.Status.MATCHED
PARTIALLY_MATCHED = OrderStatus.Status.PARTIALLY_MATCHED
TRADE_BROKEN = OrderStatus.Status.TRADE_BROKEN