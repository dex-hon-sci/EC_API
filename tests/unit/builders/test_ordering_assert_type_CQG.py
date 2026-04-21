import pytest
from datetime import datetime, timezone
from EC_API.ordering.enums import (
    Side, 
    Duration, 
    OrderType,
    ExecInstruction
    )
from EC_API.ordering.cqg.builders import (
    build_new_order_request_msg,
    build_modify_order_request_msg,
    build_cancel_order_request_msg,
    build_activate_order_request_msg,
    build_cancelall_order_request_msg,
    build_liquidateall_order_request_msg,
    build_goflat_order_request_msg
    )
from EC_API.exceptions import MsgBuilderError

def test_check_crendential_fail_TypeError() -> None:
    wrong_type = {
        #"symbol_name": 00000, # Wrong type input in symbol_name
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.AON
        }
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = "0", # Wrong type input in symbol_name
            **wrong_type
            )

def test_check_request_specific_fields_NEW_ORDER_fail_TypeError() -> None:
    wrong_type = {
        ##"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": 0, # <== wrong type 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.AON
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **wrong_type
            )
        
def test_check_request_specific_fields_NEW_ORDER_is_manual_fail_TypeError() -> None:
    wrong_type = {
        "cl_order_id": "1231314",
        "order_type": "0",  
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": 0, # <--- wrong type, bool is int sub type
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.AON
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **wrong_type
            )

def test_check_request_specific_fields_MODIFY_ORDER_fail_TypeError( ) -> None:
    wrong_type = {
        #"symbol_name": "CLEV25",
        "orig_cl_order_id": "1231311",
        "cl_order_id": "1231314",
        "scaled_limit_price": float(1000.0), #<== wrong type, float is not accepted
        }
    
    with pytest.raises(MsgBuilderError):
        build_modify_order_request_msg(
            account_id=0, 
            request_id = 0, 
            order_id= '0', 
            **wrong_type
            )

def test_check_request_specific_fields_CANCEL_ORDER_fail_TypeError() -> None:
    wrong_type = {
        ##"symbol_name": "CLEV25",
        "orig_cl_order_id": 1231311, # <-- wrong type
        "cl_order_id": "1231314",
        }
    
    with pytest.raises(MsgBuilderError):
        build_cancel_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            order_id = '0', 
            **wrong_type
            )
def test_check_request_specific_fields_ACTIVATE_ORDER_fail_TypeError() -> None:
    wrong_type = {
        ##"symbol_name": "CLEV25",
        "orig_cl_order_id": 1231311, # <-- wrong type
        "cl_order_id": "1231314",
        'when_utc_timestamp': datetime.now(tz=timezone.utc)
        }
    
    with pytest.raises(MsgBuilderError):
        build_activate_order_request_msg(
            account_id = 0,
            request_id = 0,
            order_id = '0',
            **wrong_type
            )

def test_check_request_specific_fields_CANCELALL_ORDER_fail_TypeError() -> None:
    wrong_type = {
        }
    
    with pytest.raises(MsgBuilderError):
        build_cancelall_order_request_msg(
            account_id = 0,
            request_id = 0,
            cl_order_id = 0, # <== wrong type
            **wrong_type
            )

def test_check_request_specific_fields_GOFLAT_ORDER_fail_TypeError() -> None:
    wrong_type = {
        #"symbol_name": "CLEV25",
        'when_utc_timestamp': 0000, #<-- wrong type, should be datetime
        }
    
    with pytest.raises(MsgBuilderError):
        build_goflat_order_request_msg(
            account_id = 0,
            request_id = 0,
            **wrong_type
            )

def test_check_order_specific_essential_fields_LMT_fail_TypeError()-> None:
    wronginput_input = {
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000.0, # <-- wrong type for LMT price 
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **wronginput_input
            )
        
def test_check_order_specific_essential_fields_STP_fail_TypeError():
    wronginput_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_stop_price": 1000.0, # <-- wrong type for STP price 
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **wronginput_input
            )

def test_check_order_specific_essential_fields_STL_fail_TypeError()-> None:
    wronginput_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STL, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000.0, # <-- wrong type for LMT price 
        "scaled_stop_price": 1000.0, # <-- wrong type for LMT price 
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,  
            **wronginput_input
            )

def test_check_order_specific_essential_fields_GTD_fail_TypeError()-> None:
    wronginput_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT,
        "duration": Duration.GTD, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "good_thru_date": datetime(2025,8,9) # <-- wrong type for good_thru_date, should be int 
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,  
            **wronginput_input
            )

def test_check_order_specific_essential_fields_Trail_fail_TypeError() -> None:
    wronginput_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT,
        "duration": Duration.GTD, 
        "side": Side.BUY,
        "qty_significant": 2,
        "qty_exponent": 0, 
        "is_manual": False,
        "scaled_limit_price": 1000,
        "exec_instructions": ExecInstruction.TRAIL,
        "scaled_trail_offset": 100.0 # <---- wrong type should be int
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,  
            **wronginput_input
            )