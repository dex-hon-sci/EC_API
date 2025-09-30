#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 18:38:26 2025

@author: dexter
"""
# In the Future we need a Strategy scanner machine that check compliance of 
# a strategy, for example, scan if the strategy action tree ultimately 
# have an equal qty of Buy/Sell orders (balance check).
from datetime import datetime, timedelta, timezone
from EC_API.op_strategy.action import ActionNode, ActionTree
from EC_API.op_strategy.signal import OpSignal
from EC_API.payload.cqg.safety import CQGFormatCheck
from EC_API.payload.base import Payload
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType, OrderType, Duration, Side, ExecInstruction

# Global variables
ACCOUNT_ID = 100
checks = CQGFormatCheck #Define checking schema for Payloads

# Trigger Conditions
# a, b, c, d, a2 = 100, 50, 60, 70, 80
TE_trigger =  lambda ctx: ctx.price >= 100
mod_TE_trigger = lambda ctx: 50 < ctx.price < 100
TP_trigger_1 = lambda ctx: ctx.price <= 60
TP_trigger_2 = lambda ctx: ctx.price <= 70
cancel_trigger = lambda ctx: ctx.price < 50
overtime_cond = lambda ctx: ctx.timestamp >= (datetime.now(tz=timezone.utc) + timedelta(seconds=5)).timestamp()

# Define Payloads for asset A
TE_PL_A = Payload(  
    account_id=ACCOUNT_ID,
    request_id=101,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.NEW_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_SELL,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 100,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
        },
    check_method = checks
    )
TE_mod_PL_A = Payload(
    account_id=ACCOUNT_ID,
    request_id=102,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.MODIFY_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",
        "orig_cl_order_id" : "1231314",
        "cl_order_id" : "1231315",
        "scaled_limit_price": 80, 
        },
    check_method = checks
    )
TP_PL1_A = Payload(
    account_id=ACCOUNT_ID,
    request_id=103,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.NEW_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "scaled_limit_price": 60,
        },
    check_method = checks
    )
TP_PL2_A = Payload(
    account_id=ACCOUNT_ID,
    request_id=104,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.NEW_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "scaled_limit_price": 70,
        },
    check_method = checks
    )
cancel_PL_A = Payload(
    account_id=ACCOUNT_ID,
    request_id=105,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.CANCEL_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",
        "orig_cl_order_id": "1231314", 
        "cl_order_id": "1231315",
        },
    check_method = checks
    )
overtime_PL_A = Payload(
    account_id=ACCOUNT_ID,
    request_id=106,
    status = PayloadStatus.PENDING,
    order_request_type = RequestType.LIQUIDATEALL_ORDER,
    start_time = datetime.now(timezone.utc) +\
                 timedelta(minutes=5),
    end_time = datetime.now(timezone.utc) +\
               timedelta(days=1),
    order_info = {
        "symbol_name": "Asset_A",

        },
    check_method = checks
    )

# Define Action Nodes
cancel_node = ActionNode("CancelEntry", 
                         payloads = [cancel_PL_A], 
                         trigger_cond = cancel_trigger, 
                         transitions={})
TP_node_1 = ActionNode("TakeProfit1", 
                       payloads=[TP_PL1_A], 
                       trigger_cond = TP_trigger_1, 
                       transitions={})
TP_node_2 = ActionNode("TakeProfit2", 
                       payloads =[TP_PL2_A], 
                       trigger_cond = TP_trigger_2, 
                       transitions={})
TE_node_mod = ActionNode("ModifyTargetEntry", 
                         payloads=[TE_mod_PL_A], 
                         trigger_cond = mod_TE_trigger, 
                         transitions={
                             "TakeProfit2": (TP_trigger_2, TP_node_2)
                             })
TE_node = ActionNode("TargetEntry", 
                     payloads=[TE_PL_A], # Have two assets for testing. Same direction
                     trigger_cond = TE_trigger, 
                     transitions = { # Same transition and trigger conditions
                         "TakeProfit1": (TP_trigger_1, TP_node_1),
                         "ModifyTargetEntry": (mod_TE_trigger, TE_node_mod),
                         "CancelEntry": (cancel_trigger, cancel_node)   
                         })
overtime_node = ActionNode("OvertimeExit", 
                           payloads=[overtime_PL_A], 
                           trigger_cond=overtime_cond, 
                           transitions={})

# Define Action Tree
tree = ActionTree(TE_node, overtime_cond, overtime_node)

# Define OpSignal
OPS = OpSignal()
# Define OpStrategy





def test_action_sequence_TP1() -> None:
    pass

def test_action_sequence_mod_TP2() -> None:
    pass

def test_action_sequence_cancel() -> None:
    pass

def test_action_sequence_overtime() -> None:
    pass
