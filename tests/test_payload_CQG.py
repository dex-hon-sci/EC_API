#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 16:18:22 2025

@author: dexter
"""
from datetime import datetime,timezone, timedelta
from EC_API.payload.base import Payload
from EC_API.paylaod.enums import PayloadStatus, RequestType
from EC_API.payload.CQG_safety import CQGFormatCheck
from EC_API.ordering.enums import *

# test Payload construction
def test_payload_construction_succes() -> None:
    ORDER_INFO = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": ORDER_TYPE_LMT, 
        "duration": DURATION_GTC, 
        "side": SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": EXEC_INSTRUCTION_AON
        }
    PL1 = Payload(
          request_id = 100,
          status = PayloadStatus.PENDING,
          order_request_type = RequestType.NEW_ORDER,
          start_time = datetime.now(timezone.utc),
          end_time = datetime.now(timezone.utc)+timedelta(days=1),
          order_info = ORDER_INFO,
          check_method = CQGFormatCheck
          )
    assert type(PL1) == Payload

# test PayloadFormatCheck
# - test check_crendential
def test_CQGFormatCheck_check_crendential_success() -> None:
    pass

def test_CQGFormatCheck_check_crendential_fail_null() -> None:
    null_input = {
        "symbol_name": "",
        "cl_order_id": "1231314",
        "order_type": ORDER_TYPE_LMT, 
        "duration": DURATION_GTC, 
        "side": SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": EXEC_INSTRUCTION_AON
        }
    with pytest.raises(KeyError, match=r"Essential parameter(s): symbol_name is missing"):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck
            )

def test_CQGFormatCheck_check_crendential_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": 00000, # Wrong type input in symbol_name
        "cl_order_id": "1231314",
        "order_type": ORDER_TYPE_LMT, 
        "duration": DURATION_GTC, 
        "side": SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": EXEC_INSTRUCTION_AON
        }
    with pytest.raises(TypeError, match=r"Type Error, symbol_name must be: str"):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck
            )
        
# - check_request_specific_fields (NEW_ORDER, MODIFY_ORDER, CANCEL_ORDER, 
# ACRIVATE_ORDER, CANCELALL_ORDER, LIQUIDATEALL_ORDER, GOFLAT_ORDER)
def test_CQGFormatCheck_check_request_specific_fields_NEW_ORDER_fail_null():
    null_input = {
        "symbol_name": "",
        "cl_order_id": "1231314",
        "order_type": ORDER_TYPE_LMT, 
        "duration": DURATION_GTC, 
        "side": SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": EXEC_INSTRUCTION_AON
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter(s): symbol_name is missing"):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck
            )


def test_CQGFormatCheck_check_request_specific_fields_NEW_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_MODIFY_ORDER_fail_null():
    pass

def test_CQGFormatCheck_check_request_specific_fields_MODIFY_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_CANCEL_ORDER_fail_null():
    pass

def test_CQGFormatCheck_check_request_specific_fields_CANCEL_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_CANCEL_ORDER_fail_null():
    pass

def test_CQGFormatCheck_check_request_specific_fields_ACRIVATE_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_ACRIVATE_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_CANCELALL_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_CANCELALL_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_LIQUIDATEALL_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_LIQUIDATEALL_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_GOFLAT_ORDER_fail_TypeError():
    pass

def test_CQGFormatCheck_check_request_specific_fields_GOFLAT_ORDER_fail_TypeError():
    pass

# - check_order_specific_essential_fields (ORDER_TYPE_LMT, ORDER_TYPE_STP, 
#                                           ORDER_TYPE_STL, GTD Trail)
# - check_valid_value
# full run

# test ExecutePayload_CQG (PENDING, NOT PENDING, STATUS changes)