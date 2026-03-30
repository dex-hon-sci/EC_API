#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 06:52:02 2025

@author: dexter
"""
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as CQG_TS
from EC_API.ext.WebAPI.order_2_pb2 import Order as CQG_Ord
from EC_API.ext.common.shared_1_pb2 import OrderStatus as CQG_OrdStatus
from EC_API.ordering.enums import (
    SubScope, Side, OrderType,
    Duration, ExecInstruction,
    OrderStatus
    )
from EC_API.ordering.cqg.enums import (
    SubScopeCQG, OrderTypeCQG,
    DurationCQG, ExecInstructionCQG,
    )

# Vendor Enum -> Int Enum (Int Regular+Int vendor) -> Payload Enum
# This mapping file translate between Vendor Enum <-> Int Enum
SubScope_MAP_INT2CQG = {
    SubScope.ORDERS: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ORDERS,
    SubScope.POSITIONS: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_POSITIONS,
    SubScopeCQG.COLLATERAL: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_COLLATERAL,
    SubScope.ACCOUNT_SUMMARY: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY,
    SubScopeCQG.EXCHANGE_POSITIONS: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS,
    SubScopeCQG.EXCHANGE_BALANCES: CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_BALANCES    
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
    OrderTypeCQG.CROSS: CQG_Ord.OrderType.ORDER_TYPE_CROSS
    }

Duration_MAP_INT2CQG = {
    Duration.DAY: CQG_Ord.Duration.DURATION_DAY,
    Duration.GTC: CQG_Ord.Duration.DURATION_GTC,
    Duration.GTD: CQG_Ord.Duration.DURATION_GTD,
    Duration.FOK: CQG_Ord.Duration.DURATION_FOK,
    DurationCQG.GTT: CQG_Ord.Duration.DURATION_GTT,
    DurationCQG.FAK: CQG_Ord.Duration.DURATION_FAK,
    DurationCQG.ATO: CQG_Ord.Duration.DURATION_ATO,
    DurationCQG.ATC: CQG_Ord.Duration.DURATION_ATC,
    DurationCQG.GFA: CQG_Ord.Duration.DURATION_GFA
    }

ExecInstruction_MAP_INT2CQG = {
    ExecInstruction.NONE: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_NONE,
    ExecInstruction.AON: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_AON,
    ExecInstruction.ICEBERG: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ICEBERG,
    ExecInstruction.TRAIL: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_TRAIL,
    ExecInstructionCQG.FUNARI: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_FUNARI,
    ExecInstructionCQG.MIT: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MIT,
    ExecInstructionCQG.MLM: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MLM,
    ExecInstruction.POSTONLY: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_POSTONLY,
    ExecInstructionCQG.MTL: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MTL,
    ExecInstructionCQG.AUCTION: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_AUCTION,
    ExecInstructionCQG.ATANYPRICE: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ATANYPRICE,
    ExecInstructionCQG.LMT_PRARGD: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_LMT_PRARGD,
    ExecInstructionCQG.ICO: CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_ICO
    }

OrderStatus_MAP_INT2CQG = {
    CQG_OrdStatus.Status.IN_TRANSIT: OrderStatus.PENDING,
    CQG_OrdStatus.Status.REJECTED: OrderStatus.REJECTED,
    CQG_OrdStatus.Status.WORKING: OrderStatus.OPEN,
    CQG_OrdStatus.Status.EXPIRED: OrderStatus.EXPIRED,
    CQG_OrdStatus.Status.IN_CANCEL: OrderStatus.PENDING,
    CQG_OrdStatus.Status.IN_MODIFY: OrderStatus.PENDING,
    CQG_OrdStatus.Status.CANCELLED: OrderStatus.CANCELLED,
    CQG_OrdStatus.Status.FILLED: OrderStatus.FILLED,
    CQG_OrdStatus.Status.SUSPENDED: OrderStatus.OPEN,
    CQG_OrdStatus.Status.DISCONNECTED: OrderStatus.ERROR,
    CQG_OrdStatus.Status.ACTIVEAT: OrderStatus.PENDING,
    CQG_OrdStatus.Status.APPROVE_REQUIRED: OrderStatus.PENDING, #OrderStatus.APPROVE_REQUIRED,
    CQG_OrdStatus.Status.APPROVED_BY_EXCHANGE: OrderStatus.OPEN, #OrderStatus.APPROVED_BY_EXCHANGE,
    CQG_OrdStatus.Status.APPROVE_REJECTED: OrderStatus.REJECTED,
    CQG_OrdStatus.Status.MATCHED: OrderStatus.FILLED,#OrderStatus.MATCHED,
    CQG_OrdStatus.Status.PARTIALLY_MATCHED: OrderStatus.PARTIAL,#OrderStatus.PARTIALLY_MATCHED,
    CQG_OrdStatus.Status.TRADE_BROKEN: OrderStatus.ERROR,
    }



 