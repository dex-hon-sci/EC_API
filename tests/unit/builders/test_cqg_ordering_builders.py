#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:43:55 2025

@author: dexter
"""
from datetime import datetime, timezone, timedelta
from EC_API.ext.WebAPI.order_2_pb2 import Order as CQG_Ord
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscription as CQG_TS
from EC_API.ordering.enums import Duration, Side, OrderType
from EC_API.ordering.cqg.enums import DurationCQG, ExecInstructionCQG, SubScopeCQG
from EC_API.ordering.cqg.builders import (
    build_trade_subscription_msg,
    build_new_order_request_msg,
    build_modify_order_request_msg,
    build_cancel_order_request_msg,
    build_activate_order_request_msg,
    build_goflat_request_msg,
    )

ACCOUNT_ID = 000000
REQUEST_ID = 100

def test_build_trade_subscription_msg_valid() -> None:
    msg = build_trade_subscription_msg(
        10, subscribe= True,
        sub_scope = SubScopeCQG.EXCHANGE_POSITIONS,
        skip_orders_snapshot = True
        )
                          
    assert msg.trade_subscriptions[0].id == 10
    assert msg.trade_subscriptions[0].subscribe == True
    assert msg.trade_subscriptions[0].skip_orders_snapshot == True 
    assert msg.trade_subscriptions[0].subscription_scopes[0] == CQG_TS.SubscriptionScope.SUBSCRIPTION_SCOPE_EXCHANGE_POSITIONS

def test_build_new_order_request_msg_valid() -> None:
    
    DT = datetime.now(timezone.utc)
    GTD = DT + timedelta(days=1)
    
    msg = build_new_order_request_msg(
        ACCOUNT_ID, REQUEST_ID,
        contract_id = 10, # Get this from contractmetadata
        cl_order_id = "cl001", 
        order_type = OrderType.STP, 
        duration =  Duration.GTC, 
        side = Side.SELL, # Delibrate choice here to return error msg if no side is provided
        qty_significant = 111, # make sure qty are in Decimal (int) not float
        qty_exponent = 2, 
        is_manual = True,
        exec_instructions = ExecInstructionCQG.MLM,
        good_thru_date = 90000,
        scaled_limit_price = 10121, 
        scaled_stop_price = 10235,
        when_utc_timestamp = DT,
        suspend = True,
        scaled_trail_offset = 50,
        good_thru_utc_timestamp =  GTD,
        algo_strategy = "Kaka")
    assert msg.order_requests[0].request_id == REQUEST_ID
    assert msg.order_requests[0].new_order.order.account_id == ACCOUNT_ID
    assert msg.order_requests[0].new_order.order.contract_id == 10
    assert msg.order_requests[0].new_order.order.cl_order_id == "cl001"
    assert msg.order_requests[0].new_order.order.order_type == CQG_Ord.OrderType.ORDER_TYPE_STP
    assert msg.order_requests[0].new_order.order.duration == CQG_Ord.Duration.DURATION_GTC
    assert msg.order_requests[0].new_order.order.side == CQG_Ord.Side.SIDE_SELL
    assert msg.order_requests[0].new_order.order.qty.significand == 111
    assert msg.order_requests[0].new_order.order.qty.exponent == 2
    assert msg.order_requests[0].new_order.order.is_manual == True
    assert msg.order_requests[0].new_order.order.exec_instructions[0] == CQG_Ord.ExecInstruction.EXEC_INSTRUCTION_MLM
    assert msg.order_requests[0].new_order.order.good_thru_date == 90000
    assert msg.order_requests[0].new_order.order.scaled_limit_price == 10121
    assert msg.order_requests[0].new_order.order.scaled_stop_price == 10235
    assert msg.order_requests[0].new_order.order.when_utc_timestamp.seconds == int(DT.timestamp())
    assert msg.order_requests[0].new_order.order.when_utc_timestamp.nanos == DT.microsecond * 1000
    assert msg.order_requests[0].new_order.suspend == True
    assert msg.order_requests[0].new_order.order.scaled_trail_offset == 50
    assert msg.order_requests[0].new_order.order.good_thru_utc_timestamp.seconds == int(GTD.timestamp())
    assert msg.order_requests[0].new_order.order.good_thru_utc_timestamp.nanos == GTD.microsecond * 1000
    assert msg.order_requests[0].new_order.order.algo_strategy == "Kaka"
    

def test_build_modify_order_request_msg_valid() -> None:
    mod_datetime = datetime.now(timezone.utc)
    goodthru_datetime = mod_datetime + timedelta(hours=1)
    activation_datetime = mod_datetime + timedelta(hours=2)
    
    msg = build_modify_order_request_msg(
        ACCOUNT_ID, REQUEST_ID,
        order_id = "200", 
        orig_cl_order_id = "300",
        cl_order_id = "400",
        when_utc_timestamp = mod_datetime,
        qty = 27, 
        scaled_limit_price = 12300,
        scaled_stop_price = 12400,
        remove_activation_time = True,
        remove_suspension_utc_time = True,
        duration = DurationCQG.ATC, 
        good_thru_date = 10001,
        good_thru_utc_timestamp = goodthru_datetime, 
        activation_utc_timestamp = activation_datetime,
        extra_attributes = None,
        )
    assert msg.order_requests[0].request_id == REQUEST_ID
    assert msg.order_requests[0].modify_order.account_id == ACCOUNT_ID
    assert msg.order_requests[0].modify_order.order_id == "200"
    assert msg.order_requests[0].modify_order.orig_cl_order_id == "300"
    assert msg.order_requests[0].modify_order.cl_order_id == "400"
    assert msg.order_requests[0].modify_order.when_utc_timestamp.seconds == int(mod_datetime.timestamp())
    assert msg.order_requests[0].modify_order.when_utc_timestamp.nanos == mod_datetime.microsecond * 1000
    assert msg.order_requests[0].modify_order.qty.significand == 27
    assert msg.order_requests[0].modify_order.qty.exponent == 0
    assert msg.order_requests[0].modify_order.scaled_limit_price == 12300
    assert msg.order_requests[0].modify_order.scaled_stop_price == 12400
    assert msg.order_requests[0].modify_order.remove_activation_time == True
    assert msg.order_requests[0].modify_order.remove_suspension_utc_time == True
    assert msg.order_requests[0].modify_order.duration == CQG_Ord.Duration.DURATION_ATC
    assert msg.order_requests[0].modify_order.good_thru_date == 10001
    assert msg.order_requests[0].modify_order.good_thru_utc_timestamp.seconds == int(goodthru_datetime.timestamp())
    assert msg.order_requests[0].modify_order.good_thru_utc_timestamp.nanos == goodthru_datetime.microsecond * 1000
    assert msg.order_requests[0].modify_order.activation_utc_timestamp.seconds == int(activation_datetime.timestamp())
    assert msg.order_requests[0].modify_order.activation_utc_timestamp.nanos == activation_datetime.microsecond * 1000

def test_build_cancel_order_request_msg_valid() -> None:
    DT = datetime.now(timezone.utc)
    msg = build_cancel_order_request_msg(
        ACCOUNT_ID, REQUEST_ID,
        order_id = "70", 
        orig_cl_order_id = "og_cl001", 
        cl_order_id = "cl002",
        when_utc_timestamp = DT
        )
    assert msg.order_requests[0].request_id == REQUEST_ID
    assert msg.order_requests[0].cancel_order.account_id == ACCOUNT_ID
    assert msg.order_requests[0].cancel_order.order_id == "70"
    assert msg.order_requests[0].cancel_order.orig_cl_order_id == "og_cl001"
    assert msg.order_requests[0].cancel_order.cl_order_id == "cl002"
    assert msg.order_requests[0].cancel_order.when_utc_timestamp.seconds == int(DT.timestamp())
    assert msg.order_requests[0].cancel_order.when_utc_timestamp.nanos == DT.microsecond * 1000
    
def test_build_cancelall_order_request_msg_valid() -> None:
    pass

def test_build_suspend_order_request_msg_valid() -> None:
    pass

def test_build_activate_order_request_msg_valid() -> None:
    DT = datetime.now(timezone.utc)
    msg = build_activate_order_request_msg(
        account_id = ACCOUNT_ID, 
        request_id = REQUEST_ID, 
        order_id = "ORD_ID001", 
        orig_cl_order_id = "og1001", 
        cl_order_id = "1002", 
        when_utc_timestamp=DT
        )
    assert msg.order_requests[0].request_id == REQUEST_ID
    assert msg.order_requests[0].activate_order.account_id == ACCOUNT_ID
    assert msg.order_requests[0].activate_order.order_id == "ORD_ID001"
    assert msg.order_requests[0].activate_order.orig_cl_order_id == "og1001"
    assert msg.order_requests[0].activate_order.cl_order_id == "1002"
    assert msg.order_requests[0].activate_order.when_utc_timestamp.seconds == int(DT.timestamp())
    assert msg.order_requests[0].activate_order.when_utc_timestamp.nanos == DT.microsecond * 1000

def test_build_liquidateall_order_request_msg_valid() -> None:
    pass

def test_build_goflat_order_request_msg_valid() -> None:
    goflat_datetime = datetime.now(timezone.utc)

    msg = build_goflat_request_msg(
        ACCOUNT_ID, REQUEST_ID,
        when_utc_timestamp = goflat_datetime,
        execution_source_code = "Goflat_unit_test", 
        speculation_type = 1 # SpeculationType Enum, fix this late
        )

    assert msg.order_requests[0].request_id == REQUEST_ID
    assert msg.order_requests[0].go_flat.account_ids[0] == ACCOUNT_ID
    assert msg.order_requests[0].go_flat.when_utc_timestamp.seconds == int(goflat_datetime.timestamp())
    assert msg.order_requests[0].go_flat.when_utc_timestamp.nanos == goflat_datetime.microsecond * 1000
    assert msg.order_requests[0].go_flat.execution_source_code == "Goflat_unit_test"
    assert msg.order_requests[0].go_flat.speculation_type == 1