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


# test Payload construction
def test_payload_construction_succes() -> None:
    ORDER_INFO = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.AON
        }
    PL1 = Payload(
          request_id = 100,
          status = PayloadStatus.PENDING,
          order_request_type = RequestType.NEW_ORDER,
          start_time = datetime.now(timezone.utc),
          end_time = datetime.now(timezone.utc)+timedelta(days=1),
          order_info = ORDER_INFO,
          check_method = CQGFormatCheck,
          asset_safty_range = ASSETS_SAFETY_RANGE
          )
    assert type(PL1) == Payload

# test PayloadFormatCheck
def test_CQGFormatCheck_check_crendential_fail_null() -> None:
    null_input = {
        "symbol_name": None, # missing symbol_name
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        }
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): symbol_name is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )
    #print(PL)
    
#test_CQGFormatCheck_check_crendential_fail_null()
def test_CQGFormatCheck_check_crendential_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": 00000, # Wrong type input in symbol_name
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
        }
    with pytest.raises(TypeError, match="Type Error, symbol_name must be: str."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )
        
# - check_request_specific_fields (NEW_ORDER, MODIFY_ORDER, CANCEL_ORDER, 
# ACRIVATE_ORDER, CANCELALL_ORDER, LIQUIDATEALL_ORDER, GOFLAT_ORDER)
def test_CQGFormatCheck_check_request_specific_fields_NEW_ORDER_fail_null() -> None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        #"order_type": ORDER_TYPE_LMT, 
        #"duration": DURATION_GTC, 
        #"side": SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): order_type is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )


def test_CQGFormatCheck_check_request_specific_fields_NEW_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": 0, # <== wrong type 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_AON
        }
    
    with pytest.raises(TypeError, match=r"Type Error, order_type must be: OrderType."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_MODIFY_ORDER_fail_null() -> None:
    null_input = {
        "symbol_name": "CLEV25",
        #"cl_order_id": "1231314",#<== missing parameter
        "scaled_limit_price": 1000.0, 
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): orig_cl_order_id is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.MODIFY_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_MODIFY_ORDER_fail_TypeError( ) -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        "orig_cl_order_id": "1231311",
        "cl_order_id": "1231314",
        "scaled_limit_price": float(1000.0), #<== wrong type, float is not accepted
        }
    
    with pytest.raises(TypeError, match=r"Type Error, scaled_limit_price must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.MODIFY_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_CANCEL_ORDER_fail_null() -> None:
    null_input = {
        "symbol_name": "CLEV25",
        "orig_cl_order_id": "1231315"
        #"cl_order_id": "1231314",#<== missing parameter
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): cl_order_id is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.CANCEL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_CANCEL_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        "orig_cl_order_id": 1231311, # <-- wrong type
        "cl_order_id": "1231314",
        }
    
    with pytest.raises(TypeError, match=r"Type Error, orig_cl_order_id must be: str."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.CANCEL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_ACTIVATE_ORDER_fail_null() -> None:
    null_input = {
        "symbol_name": "CLEV25",
        "orig_cl_order_id": "1231315"
        #"cl_order_id": "1231314",#<== missing parameter
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): cl_order_id is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.ACTIVATE_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_ACTIVATE_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        "orig_cl_order_id": 1231311, # <-- wrong type
        "cl_order_id": "1231314",
        }
    
    with pytest.raises(TypeError, match=r"Type Error, orig_cl_order_id must be: str."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.ACTIVATE_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_CANCELALL_ORDER_fail_null() -> None:
    null_input = {
        "symbol_name": "CLEV25",
        #"cl_order_id": "1231314",#<== missing parameter
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): cl_order_id is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.CANCELALL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_CANCELALL_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        "cl_order_id": 1231314, # <-- wrong type
        }
    
    with pytest.raises(TypeError, match=r"Type Error, cl_order_id must be: str."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.CANCELALL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_LIQUIDATEALL_ORDER_fail_notaccept() -> None:
    notaccept_input = {
        "symbol_name": "CLEV25",
        "islong": "1231315",#<== not accepteable parameter
        }
    
    with pytest.raises(AttributeError, match=r"islong is not an acceptable field for RequestType.LIQUIDATEALL_ORDER request."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.LIQUIDATEALL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = notaccept_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_LIQUIDATEALL_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        'when_utc_timestamp': 0000, #<-- wrong type, should be datetime
        }
    
    with pytest.raises(TypeError, match=r"Type Error, when_utc_timestamp must be: datetime."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.LIQUIDATEALL_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_GOFLAT_ORDER_fail_notaccept() -> None:
    notaccept_input = {
        "symbol_name": "CLEV25",
        "when_utc": "1231315",#<== not accepteable parameter
        }
    
    with pytest.raises(AttributeError, match=r"when_utc is not an acceptable field for RequestType.GOFLAT_ORDER request."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.GOFLAT_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = notaccept_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_request_specific_fields_GOFLAT_ORDER_fail_TypeError() -> None:
    wrong_type = {
        "symbol_name": "CLEV25",
        'when_utc_timestamp': 0000, #<-- wrong type, should be datetime
        }
    
    with pytest.raises(TypeError, match=r"Type Error, when_utc_timestamp must be: datetime."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.GOFLAT_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wrong_type,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )


# - check_order_specific_essential_fields         
def test_CQGFormatCheck_check_order_specific_essential_fields_LMT_fail_null()->None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        #"scaled_limit_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): scaled_limit_price is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )


def test_CQGFormatCheck_check_order_specific_essential_fields_STP_fail_null()->None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_STP, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        #"scaled_stop_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): scaled_stop_price is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_STL_fail_null()->None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_STL, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        #"scaled_limit_price": 1000, <-- missing stop price
        #"scaled_stop_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): scaled_limit_price is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_GTD_fail_null()->None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTD, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000, 
        #"good_thru_date": 10, <-- missing good_thru_date price
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): good_thru_date is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_Trail_fail_null()-> None:
    null_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000, 
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_TRAIL,
        #"scaled_trail_offset": 10, <-- missing scaled_trail_offset price
        }
    
    with pytest.raises(KeyError, match=r"Essential parameter\(s\): scaled_trail_offset is missing."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = null_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_LMT_fail_TypeError()-> None:
    wronginput_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000.0, # <-- wrong type for LMT price 
        }
    
    with pytest.raises(TypeError, match=r"Type Error, scaled_limit_price must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wronginput_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_STP_fail_TypeError():
    wronginput_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_STP, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 1000.0, # <-- wrong type for LMT price 
        }
    
    with pytest.raises(TypeError, match=r"Type Error, scaled_stop_price must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wronginput_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_STL_fail_TypeError()-> None:
    wronginput_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_STL, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000.0, # <-- wrong type for LMT price 
        "scaled_stop_price": 1000.0, # <-- wrong type for LMT price 
        }
    
    with pytest.raises(TypeError, match=r"Type Error, scaled_limit_price must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wronginput_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )


def test_CQGFormatCheck_check_order_specific_essential_fields_GTD_fail_TypeError()-> None:
    wronginput_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT,
        "duration": Duration.DURATION_GTD, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,8,9) # <-- wrong type for good_thru_date, should be int 
        }
    
    with pytest.raises(TypeError, match=r"Type Error, good_thru_date must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wronginput_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

def test_CQGFormatCheck_check_order_specific_essential_fields_Trail_fail_TypeError() -> None:
    wronginput_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT,
        "duration": Duration.DURATION_GTD, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_TRAIL,
        "scaled_trail_offset": 100.0 # <---- wrong type should be int
        }
    
    with pytest.raises(TypeError, match=r"Type Error, scaled_trail_offset must be: int."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = wronginput_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

# - check_valid_value
def test_CQGFormatCheck_check_valid_value_LMT_price_up() -> None:
    outoflimit_input = {
        "symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 15000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_limit_price is outside of the allowed range: \[100, 10000\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 90, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_limit_price is outside of the allowed range: \[100, 10000\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_STP, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 16000, # <-- more than allowed limit
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_stop_price is outside of the allowed range: \[100, 15000\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_STP, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 60, # <-- less than allowed limit
        "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_NONE
        }
    
    with pytest.raises(ValueError, match=r"scaled_stop_price is outside of the allowed range: \[100, 15000\]."):
        PL = Payload(          
            request_id = 100,
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
            request_id = 100,
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
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 13, # <-- more than allowed limit
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_significant is outside of the allowed range: \[1, 9\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 0, # <-- less than allowed limit
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_significant is outside of the allowed range: \[1, 9\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 8,
        "qty_exponent": 2, # <-- more than allowed limit
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_exponent is outside of the allowed range: \[0, 1\]."):
        PL = Payload(          
            request_id = 100,
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
        "order_type": OrderType.ORDER_TYPE_LMT, 
        "duration": Duration.DURATION_GTC, 
        "side": Side.SIDE_BUY,
        "qty_significant": 8,
        "qty_exponent": -1, # <-- less than allowed limit
        "is_manual": False,
        "scaled_limit_price": 10000, 
        "exec_instructions": ExecInstruction.NONE
        }
    
    with pytest.raises(ValueError, match=r"qty_exponent is outside of the allowed range: \[0, 1\]."):
        PL = Payload(          
            request_id = 100,
            status = PayloadStatus.PENDING,
            order_request_type = RequestType.NEW_ORDER,
            start_time = datetime.now(timezone.utc),
            end_time = datetime.now(timezone.utc)+timedelta(days=1),
            order_info = outoflimit_input,
            check_method = CQGFormatCheck,
            asset_safty_range = ASSETS_SAFETY_RANGE
            )

# test ExecutePayload_CQG (PENDING, NOT PENDING, STATUS changes)