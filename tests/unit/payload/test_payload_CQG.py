#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 12 16:18:22 2025

@author: dexter
"""
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta
from EC_API.payload.base import Payload
from EC_API.payload.safety import PreTradeRiskCheck
from EC_API.ordering.enums import RequestType
from EC_API.ordering.enums import (
    Side, 
    Duration, 
    OrderType,
    ExecInstruction
    )
from EC_API.exceptions import RiskViolationError

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
TEST_RISK_CONFIG = FIXTURES_DIR / "test_payload_check.toml"

def test_payload_check_valid_value_LMT_price_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty": 2,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "is_manual": False,
        #"scaled_limit_price": 15000, # <-- more than allowed limit
        "limit_price": 15000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    
    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )
        
def test_payload_check_valid_value_LMT_price_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty": 2,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "is_manual": False,
        #"scaled_limit_price": 90, # <-- less than allowed limit
        "limit_price": 90, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)

    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )

def test_payload_check_valid_value_STP_price_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "stop_price": 16000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)

    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )
        
def test_payload_check_valid_value_STP_price_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty": 2,
        "is_manual": False,
        "stop_price": 60, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.NONE
        }
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)

    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.NEW_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )
        
def test_payload_check_valid_value_qty_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "orig_cl_order_id" : "1313",
        "qty": 12, # <-- more than allowed limit
        }
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)

    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.MODIFY_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )
def test_payload_check_valid_value_qty_down() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231315",
        "orig_cl_order_id" : "1231314",
        "qty": 0, # <-- less than allowed limit
        }
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)

    with pytest.raises(RiskViolationError):
        Payload(          
            order_request_type = RequestType.MODIFY_ORDER,
            order_info = outoflimit_input,
            risk_check = PTRC
            )


# test ExecutePayload_CQG (PENDING, NOT PENDING, STATUS changes)