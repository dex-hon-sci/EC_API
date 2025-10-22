#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 19:22:46 2025

@author: dexter
"""
import uuid
import asyncio
from datetime import datetime, timedelta, timezone
from EC_API.op_strategy.action import ActionNode, ActionTree
from EC_API.op_strategy.signal import OpSignal
from EC_API.payload.cqg.safety import CQGFormatCheck
from EC_API.payload.base import Payload
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType, OrderType, Duration, Side, ExecInstruction

# Global variables
ACCOUNT_ID = 100
timeframe = 60 # seconds (Assume we use TimeTickBuffer)
checks = CQGFormatCheck #Define checking schema for Payloads

# Trigger Conditions 
# (a: entry LMT price, b: exit LMT price, c/d: trigger price, e: cancel order price)
# numbers: route, eg, a1 and b1 are the first route in the order chain
# Route 1, Trigger TE at c1 = 90, LMT a1=100, on_complete -> TP LMT b1 = 80, on_complete->Done
# Route 2, Trigger TE at c1 = 90, LMT a1=100, on_sent -> Tirgger mod TE if 
#          d2 (50) < price < c2 (60), mod LMT a2 = 70, on_complete-> TP LMT b2 = 40, on_complete -> Done
# Route 3, Trigger TE at c1 = 90, LMT a1=100, on_sent -> Tirgger Cancel TE if 
#          price < e3 (30), Cancel TE -> Done
price_a1, price_b1, price_a2, price_b2, \
price_c1, price_c2, price_d2, price_e3 = 100, 80, 70, 40, 90, 60, 50, 30
#price_a_up, price_a, price_b, price_c, price_d, price_a2 = 105, 100, 50, 60, 70, 80
TE_trigger =  lambda ctx: ctx.feeds['Asset_A'].tick_buffer.ohlc()['Close'] >= price_c1
mod_TE_trigger = lambda ctx: price_d2 < ctx.feeds['Asset_A'].tick_buffer.ohlc()['Close']  < price_c2
TP_trigger_1 = lambda ctx: ctx.feeds['Asset_A'].tick_buffer.ohlc()['Close']  <= price_b1
TP_trigger_2 = lambda ctx: ctx.feeds['Asset_A'].tick_buffer.ohlc()['Close']  <= price_b2
cancel_trigger = lambda ctx: ctx.feeds['Asset_A'].tick_buffer.ohlc()['Close'] < price_e3
overtime_cond = lambda ctx: ctx.feeds['Asset_A'].tick_buffer.buffers[timeframe][-1].timestamp \
                            >= (datetime.now(tz=timezone.utc) + timedelta(seconds=5)).timestamp()
ASSETS_SAFETY_RANGE = {
    "Asset_A": {'scaled_limit_price': {'upper_limit': 200, 
                                   'lower_limit': 0},
            'scaled_stop_price': {'upper_limit': 200,
                                  'lower_limit': 0},
            'qty': {'upper_limit': 10,
                    'lower_limit': 1},
            'qty_significant': {'upper_limit': 9,
                                'lower_limit': 1},
            'qty_exponent': {'upper_limit': 1,
                             'lower_limit': 0},
            },
    } # example dict # Need to make a control function for this

# Define Payloads for asset A
TE_PL_A = Payload(  
    account_id=ACCOUNT_ID,
    request_id=100,
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
        "scaled_limit_price": price_a,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
        },
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
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
        "scaled_limit_price": price_a2, 
        },
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
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
        "cl_order_id": "1231316",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "scaled_limit_price": price_c,
        },
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
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
        "cl_order_id": "1231316",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "scaled_limit_price": price_d,
        },
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
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
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
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
    check_method = checks,
    asset_safty_range = ASSETS_SAFETY_RANGE
    )
    
# Define Database for ActionNode
from tests.example_db import TEST_ASYNC_SESSION, TestStorage, init_db
DB_SESSION = TEST_ASYNC_SESSION
TO_DB_TABLE = TestStorage
SCAN_DB_TABLES = TestStorage
# Initialise test DB
asyncio.run(init_db())

# Define Action Nodes
cancel_node = ActionNode("CancelEntry", 
                         payloads = [cancel_PL_A], 
                         trigger_cond = cancel_trigger, 
                         transitions={},
                         db_session = DB_SESSION,
                         to_db_table = TO_DB_TABLE,
                         scan_db_tables = SCAN_DB_TABLES)
TP_node_1 = ActionNode("TakeProfit1", 
                       payloads=[TP_PL1_A], 
                       trigger_cond = TP_trigger_1, 
                       transitions={},
                       db_session = DB_SESSION,
                       to_db_table = TO_DB_TABLE,
                       scan_db_tables = SCAN_DB_TABLES)

TP_node_2 = ActionNode("TakeProfit2", 
                       payloads =[TP_PL2_A], 
                       trigger_cond = TP_trigger_2, 
                       transitions={},
                       db_session = DB_SESSION,
                       to_db_table = TO_DB_TABLE,
                       scan_db_tables = SCAN_DB_TABLES)

TE_node_mod = ActionNode("ModifyTargetEntry", 
                         payloads=[TE_mod_PL_A], 
                         trigger_cond = mod_TE_trigger, 
                         transitions={
                             "TakeProfit2": (TP_trigger_2, TP_node_2)
                             },
                         db_session = DB_SESSION,
                         to_db_table = TO_DB_TABLE,
                         scan_db_tables = SCAN_DB_TABLES)
TE_node = ActionNode("TargetEntry", 
                     payloads=[TE_PL_A], # Have two assets for testing. Same direction
                     trigger_cond = TE_trigger, 
                     transitions = { # Same transition and trigger conditions
                         "ModifyTargetEntry": (mod_TE_trigger, TE_node_mod),
                         "TakeProfit1": (TP_trigger_1, TP_node_1),
                         "CancelEntry": (cancel_trigger, cancel_node)   
                         },
                       db_session = DB_SESSION,
                       to_db_table = TO_DB_TABLE,
                       scan_db_tables = SCAN_DB_TABLES)
overtime_node = ActionNode("OvertimeExit", 
                           payloads=[overtime_PL_A], 
                           trigger_cond=overtime_cond, 
                           transitions={},
                           db_session = DB_SESSION,
                           to_db_table = TO_DB_TABLE,
                           scan_db_tables = SCAN_DB_TABLES)

# Define Action Tree
tree = ActionTree(TE_node, overtime_cond, overtime_node)

print('===Import ActionTree Done====')
# Define OpSignal
#OPS = OpSignal()
# Define OpStrategy