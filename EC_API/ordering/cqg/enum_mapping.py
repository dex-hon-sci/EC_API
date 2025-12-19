#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 06:52:02 2025

@author: dexter
"""
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as TS
from EC_API.ext.WebAPI.order_2_pb2 import Order as CQG_Ord
from EC_API.ext.WebAPI.order_2_pb2 import OrderStatus as CQG_OrdStatus


from EC_API.ordering.enums import (
    SubScope, Side, OrderType,
    Duration, ExecInstruction,
    OrderStatus
    )

SubScope_MAP_INT2CQG = {
    SubScope.ORDERS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS,
    SubScope.POSITIONS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS,
    SubScope.COLLATERAL: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_COLLATERAL,
    SubScope.ACCOUNT_SUMMARY: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY,
    SubScope.EXCHANGE_POSITIONS: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS,
    SubScope.EXCHANGE_BALANCES: TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES    
    }

Side_MAP_INT2CQG = {
    Side.BUY: CQG_Ord.Side.SIDE_BUY,
    Side.SELL: CQG_Ord.Side.SIDE_SELL
    }

OrderType_MAP_INT2CQG = {
    OrderType.MKT: CQG_Ord.OrderType.ORDER_TYPE_MKT,
    OrderType.LMT: CQG_Ord.OrderType.ORDER_TYPE_LMT,
    OrderType.STP: CQG_Ord.OrderType.ORDER_TYPE_STP,
    OrderType.STL: CQG_Ord.OrderType.ORDER_TYPE_STL,
    OrderType.CROSS: CQG_Ord.OrderType.ORDER_TYPE_CROSS
    }

Duration_MAP_INT2CQG = {
    Duration.DAY: CQG_Ord.Duration.DURATION_DAY,
    Duration.GTC: CQG_Ord.Duration.DURATION_GTC,
    Duration.GTD: CQG_Ord.Duration.DURATION_GTD,
    Duration.GTT: CQG_Ord.Duration.DURATION_GTT,
    Duration.FOK: CQG_Ord.Duration.DURATION_FOK,
    Duration.FAK: CQG_Ord.Duration.DURATION_FAK,
    Duration.ATO: CQG_Ord.Duration.DURATION_ATO,
    Duration.ATC: CQG_Ord.Duration.DURATION_ATC,
    Duration.GFA: CQG_Ord.Duration.DURATION_GFA
    }

ExecInstruction_MAP_INT2CQG = {
    ExecInstruction.NONE: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_NONE,
    ExecInstruction.AON: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_AON,
    ExecInstruction.ICEBERG: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ICEBERG,
    ExecInstruction.TRAIL: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL,
    ExecInstruction.FUNARI: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_FUNARI,
    ExecInstruction.MIT: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MIT,
    ExecInstruction.MLM: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MLM,
    ExecInstruction.POSTONLY: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_POSTONLY,
    ExecInstruction.MTL: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MTL,
    ExecInstruction.AUCTION: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_AUCTION,
    ExecInstruction.ATANYPRICE: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ATANYPRICE,
    ExecInstruction.LMT_PRARGD: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_LMT_PRARGD,
    ExecInstruction.ICO: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ICO,

    }

OrderStatus_MAP_INT2CQG = {
    OrderStatus.Status.IN_TRANSIT: "",
    OrderStatus.Status.REJECTED: "",
    OrderStatus.Status.WORKING: "",
    }

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

 