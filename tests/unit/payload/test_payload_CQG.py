#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 16:18:22 2025

@author: dexter
"""
import pytest
from datetime import datetime, timezone, timedelta
from EC_API.payload.base import Payload
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType
from EC_API.payload.safety import PayloadFormatCheck
from EC_API.payload.cqg.safety import CQGFormatCheck
from EC_API.ordering.enums import (
    Side, 
    Duration, 
    OrderType,
    ExecInstruction
    )

ASSETS_SAFETY_RANGE = {
    "CLEV25": {'scaled_limit_price': {'upper_limit': 10000, 
                                   'lower_limit': 100},
            'scaled_stop_price': {'upper_limit': 15000,
                                  'lower_limit': 100},
            'qty': {'upper_limit': 10,
                    'lower_limit': 1},
            'qty_significant': {'upper_limit': 9,
                                'lower_limit': 1},
            'qty_exponent': {'upper_limit': 1,
                             'lower_limit': 0},
            },
    "HOE": {},
    "Asset_A": {} # Test asset
    } # example dict # Need to make a control function for this


# - check_valid_value
def test_CQGFormatCheck_check_valid_value_LMT_price_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 15000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_limit_price is outside of the allowed range: \[100, 10000\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_LMT_price_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 90, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_limit_price is outside of the allowed range: \[100, 10000\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_STP_price_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 16000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_stop_price is outside of the allowed range: \[100, 15000\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_STP_price_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 60, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_stop_price is outside of the allowed range: \[100, 15000\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "orig_cl_order_id" : "1313",
        "cl_order_id" : "1314",
        "qty": 12, # <-- more than allowed limit
        }
    
    with pytest.raises(ValueError, match=r"qty is outside of the allowed range: \[1, 10\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.MODIFY_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231315",
        "orig_cl_order_id" : "1231314",
        "qty": 0, # <-- less than allowed limit
        }
    
    with pytest.raises(ValueError, match=r"qty is outside of the allowed range: \[1, 10\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.MODIFY_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_significant_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 13, # <-- more than allowed limit
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_significant is outside of the allowed range: \[1, 9\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_significant_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 0, # <-- less than allowed limit
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_significant is outside of the allowed range: \[1, 9\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_exponent_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 8,
        "qty_exponent": 2, # <-- more than allowed limit
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_exponent is outside of the allowed range: \[0, 1\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_valid_value_qty_exponent_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 8,
        "qty_exponent": -1, # <-- less than allowed limit
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_exponent is outside of the allowed range: \[0, 1\]."):
        PL = Payload(          
            # requesr_id= 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

# test ExecutePayload_CQG (PENDING, NOT PENDING, STATUS changes)