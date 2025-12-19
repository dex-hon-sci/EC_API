#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 06:52:02 2025

@author: dexter
"""
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from EC_API.ext.WebAPI.order_2_pb2 import Order as Ord

from EC_API.ordering.enums import (
    SubScope, Side, OrderType,
    Duration, ExecInstruction,
    OrderStatus
    )



SubScope_MAP = {
    SubScope.SUBSCRIPTION_SCOPE_ORDERS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS,
    SubScope.SUBSCRIPTION_SCOPE_POSITIONS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS,
    SubScope.SUBSCRIPTION_SCOPE_COLLATERAL: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_COLLATERAL,
    SubScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY,
    SubScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS,
    SubScope.SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES    
    }

OrderType_MAP2CQG = {
    OrderType.MKT: Ord.OrderType.ORDER_TYPE_MKT,
    OrderType.LMT: Ord.OrderType.ORDER_TYPE_LMT,
    OrderType.STP: Ord.OrderType.ORDER_TYPE_STP,
    OrderType.STL: Ord.OrderType.ORDER_TYPE_STL,
    OrderType.CROSS: Ord.OrderType.ORDER_TYPE_CROSS
    }

Duration_MAP2CQG = {
    Duration.DAY: Ord.Duration.DURATION_DAY,
    Duration.GTC: Ord.Duration.DURATION_GTC,
    Duration.GTD: Ord.Duration.DURATION_GTD,
    Duration.GTT: Ord.Duration.DURATION_GTT,
    Duration.FOK: Ord.Duration.DURATION_FOK,
    Duration.FAK: Ord.Duration.DURATION_FAK,
    Duration.ATO: Ord.Duration.DURATION_ATO,
    Duration.ATC: Ord.Duration.DURATION_ATC,
    Duration.GFA: Ord.Duration.DURATION_GFA
    }

# class ExecInstruction(Enum):
#     EXEC_INSTRUCTION_NONE = Ord.ExecInstruction.EXEC_INSTRUCTION_NONE
#     EXEC_INSTRUCTION_AON = Ord.ExecInstruction.EXEC_INSTRUCTION_AON
#     EXEC_INSTRUCTION_ICEBERG = Ord.ExecInstruction.EXEC_INSTRUCTION_ICEBERG
#     EXEC_INSTRUCTION_TRAIL = Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL
#     EXEC_INSTRUCTION_FUNARI = Ord.ExecInstruction.EXEC_INSTRUCTION_FUNARI
#     EXEC_INSTRUCTION_MIT = Ord.ExecInstruction.EXEC_INSTRUCTION_MIT
#     EXEC_INSTRUCTION_MLM = Ord.ExecInstruction.EXEC_INSTRUCTION_MLM
#     EXEC_INSTRUCTION_POSTONLY = Ord.ExecInstruction.EXEC_INSTRUCTION_POSTONLY
#     EXEC_INSTRUCTION_MTL = Ord.ExecInstruction.EXEC_INSTRUCTION_MTL
#     EXEC_INSTRUCTION_AUCTION = Ord.ExecInstruction.EXEC_INSTRUCTION_AUCTION
#     EXEC_INSTRUCTION_ATANYPRICE = Ord.ExecInstruction.EXEC_INSTRUCTION_ATANYPRICE
#     EXEC_INSTRUCTION_LMT_PRARGD = Ord.ExecInstruction.EXEC_INSTRUCTION_LMT_PRARGD
#     EXEC_INSTRUCTION_ICO = Ord.ExecInstruction.EXEC_INSTRUCTION_ICO
# 
# class OrderStatus(Enum):
#     # Define Order statuses
#     IN_TRANSIT = OrderStatus.Status.IN_TRANSIT  # Original order is sent to execution system.
#     REJECTED = OrderStatus.Status.REJECTED # Order is rejected.
#     WORKING = OrderStatus.Status.WORKING # Order is acknowledged by execution system and perhaps partially filled.
#     EXPIRED = OrderStatus.Status.EXPIRED # Order is expired.
#     IN_CANCEL = OrderStatus.Status.IN_CANCEL #Cancel request is sent to execution system.
#     IN_MODIFY = OrderStatus.Status.IN_MODIFY # Modify request is sent to execution system.
#     CANCELLED = OrderStatus.Status.CANCELLED # Order is canceled.
#     FILLED = OrderStatus.Status.FILLED # Order is completely filled by execution system.
#     SUSPENDED = OrderStatus.Status.SUSPENDED # Order is waiting submission to execution system.
#     DISCONNECTED = OrderStatus.Status.DISCONNECTED # Order may be canceled because a disconnect occurred.
#     ACTIVEAT = OrderStatus.Status.ACTIVEAT # Order will be placed at a specified time (waiting execution system to start accepting orders).
#     APPROVE_REQUIRED = OrderStatus.Status.APPROVE_REQUIRED # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
#     APPROVED_BY_EXCHANGE = OrderStatus.Status.APPROVED_BY_EXCHANGE
#     APPROVE_REJECTED = OrderStatus.Status.APPROVE_REJECTED
#     MATCHED = OrderStatus.Status.MATCHED
#     PARTIALLY_MATCHED = OrderStatus.Status.PARTIALLY_MATCHED
#     TRADE_BROKEN = OrderStatus.Status.TRADE_BROKEN
# ====================================================

 