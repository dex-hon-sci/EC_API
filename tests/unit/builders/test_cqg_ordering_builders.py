#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:43:55 2025

@author: dexter
"""
from datetime import datetime, timezone, timedelta

from EC_API.ordering.cqg.enums import Duration
from EC_API.ordering.cqg.builders import (
    build_modify_order_request_msg
    )

ACCOUNT_ID = 000000
REQUEST_ID = 100

def test_build_trade_subscription_msg_valid() -> None:
    pass

def test_build_new_order_request_msg_valid() -> None:
    pass

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
        duration = Duration.DURATION_ATC, 
        good_thru_date = 10001,
        good_thru_utc_timestamp = goodthru_datetime, 
        activation_utc_timestamp = activation_datetime,
        extra_attributes = None,
        )
    assert msg.modify_order.account_id == ACCOUNT_ID
    assert msg.modify_order.request_id == REQUEST_ID
    assert msg.modify_order.order_id == 200
    assert msg.modify_order.orig_cl_order_id == "300"
    assert msg.modify_order.cl_order_id == "400"
    assert msg.modify_order.qty == 27
    
    assert msg.modify_order.algo_strategy == "CQG Builder UNIT TEST"

def test_build_cancel_order_request_msg_valid() -> None:
    pass

def test_build_cancelall_order_request_msg_valid() -> None:
    pass

def test_build_suspend_order_request_msg_valid() -> None:
    pass

def test_build_activate_order_request_msg_valid() -> None:
    pass

def test_build_liquidateall_order_request_msg_valid() -> None:
    pass

def test_build_goflat_order_request_msg_valid() -> None:
    pass