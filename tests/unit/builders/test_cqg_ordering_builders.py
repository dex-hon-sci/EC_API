#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:43:55 2025

@author: dexter
"""
from EC_API.ordering.cqg.builders import (
    build_modify_order_request_msg_2
    )

ACCOUNT_ID = 000000
REQUEST_ID = 100

def test_build_trade_subscription_msg() -> None:
    pass

def test_build_new_order_request_msg() -> None:
    pass

def test_build_modify_order_request_msg() -> None:
    msg = build_modify_order_request_msg_2(
        ACCOUNT_ID, REQUEST_ID,
        order_id = 200, 
        orig_cl_order_id = "300",
        cl_order_id = "400"
        )
    assert msg.modify_order.account_id == ACCOUNT_ID
    assert msg.modify_order.request_id == REQUEST_ID
    assert msg.modify_order.order_id == 200
    assert msg.modify_order.orig_cl_order_id == "300"
    assert msg.modify_order.cl_order_id == "400"

def test_build_cancel_order_request_msg() -> None:
    pass

def test_build_cancelall_order_request_msg() -> None:
    pass

def test_build_suspend_order_request_msg() -> None:
    pass

def test_build_activate_order_request_msg() -> None:
    pass

def test_build_liquidateall_order_request_msg() -> None:
    pass

def test_build_goflat_order_request_msg() -> None:
    pass