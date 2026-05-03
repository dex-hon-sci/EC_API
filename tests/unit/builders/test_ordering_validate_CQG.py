import pytest
from datetime import datetime, timezone
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
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

# ---- construction test ----
def test_new_order_injection_success() -> None:
    ORDER_INFO = {
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000,
        "good_thru_date": int(datetime(2025,9,9).timestamp()),
        "exec_instructions": ExecInstruction.AON,
        "scale_factor": 1.0
        }
    client_msg = build_new_order_request_msg(
        account_id = 0, 
        request_id = 0, 
        contract_id = 0, 
        **ORDER_INFO)
    
    assert isinstance(client_msg, ClientMsg)

def test_modify_order_injection_success() -> None:
    ORDER_INFO = {
        'order_id': '0',
        'orig_cl_order_id': "111", 
        'cl_order_id': "222",
        'when_utc_timestamp': datetime.now(timezone.utc),
        "scale_factor": 1.0
        }
    client_msg = build_modify_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)

def test_cancel_order_injection_success() -> None:
    ORDER_INFO = {
        'order_id': '0',
        'orig_cl_order_id': "111", 
        'cl_order_id': "222",
        'when_utc_timestamp': datetime.now(timezone.utc)
        }
    client_msg = build_cancel_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)

def test_activate_order_injection_success() -> None:
    ORDER_INFO = {
        'order_id': '0',
        'orig_cl_order_id': "111", 
        'cl_order_id': "222",
        'when_utc_timestamp': datetime.now(timezone.utc),
        }
    client_msg = build_activate_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)

def test_cancelall_order_injection_success() -> None:
    ORDER_INFO = {
        'cl_order_id': "222",
        'when_utc_timestamp': datetime.now(timezone.utc)
        }
    client_msg = build_cancelall_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)

def test_liquidateall_order_injection_success() -> None:
    ORDER_INFO = {
        "is_short": True,
        "current_day_only": True
        }
    client_msg = build_liquidateall_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)

def test_goflat_order_injection_success() -> None:
    ORDER_INFO = {
        'when_utc_timestamp': datetime.now(timezone.utc)
        }
    client_msg = build_goflat_order_request_msg(
        account_id=0, 
        request_id=0, 
        **ORDER_INFO)
    assert isinstance(client_msg, ClientMsg)


# ---- Unknown Field inputs
def test_new_order_unknown_field_raises() -> None:
    info = {
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000,
        "good_thru_date": int(datetime(2025,9,9).timestamp()),
        "exec_instructions": ExecInstruction.AON,
        "unknown_field": 123, # <---- Unkown Field,
        "scale_factor": 1.0
        }
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, 
            request_id=0,
            contract_id=0, 
            **info)

def test_modify_order_unknown_field_raises() -> None:
    info = {
        'order_id': '0',
        'orig_cl_order_id': "111", 
        'cl_order_id': "222",
        'when_utc_timestamp': datetime.now(timezone.utc),
        "scale_factor": 1.0,
        "unknown_field": 123 # <---- Unkown Field
        }
    with pytest.raises(MsgBuilderError):
        build_modify_order_request_msg(
            account_id=0, 
            request_id=0,
            contract_id=0, 
            **info)
        
def test_liquidateall_order_unknown_field_raises() -> None:
    info = {
        'contract_id': 1,
        'cl_order_id': '1',
        "unknown_field": 123 # <---- Unkown Field
        }
    with pytest.raises(MsgBuilderError):
        build_liquidateall_order_request_msg(
            account_id=0, 
            request_id=0,
            **info)
        
def test_goflat_order_unknown_field_raises() -> None:
    info = {
        'when_utc_timestamp': datetime.now(timezone.utc),
        "unknown_field": 123 # <---- Unkown Field
        }
    with pytest.raises(MsgBuilderError):
        build_goflat_order_request_msg(
            account_id=0, 
            request_id=0,
            contract_id=0, 
            **info)

# ---- Sad path message construction 
def test_check_crendential_fail_null() -> None:
    null_input = {
        #"symbol_name": None, # missing symbol_name
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "scale_factor": 1.0
        }
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(          
            account_id = 0, 
            request_id = 0, 
            contract_id = None, # wrong contract ID type
            **null_input
            )
        
# - check_request_specific_fields (NEW_ORDER, MODIFY_ORDER, CANCEL_ORDER, 
# ACRIVATE_ORDER, CANCELALL_ORDER, LIQUIDATEALL_ORDER, GOFLAT_ORDER)
def test_check_request_specific_fields_NEW_ORDER_fail_null() -> None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        #"order_type": OrderType.ORDER_TYPE_LMT, 
        #"duration": Duration.DURATION_GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        #"is_manual": False,
        "limit_price": 1000,
        "good_thru_date": datetime(2025,9,9),
        "exec_instructions": ExecInstruction.AON,
        "scale_factor": 1.0
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **null_input
            )

def test_check_request_specific_fields_GOFLAT_ORDER_fail_notaccept() -> None:
    notaccept_input = {
        #"symbol_name": "CLEV25",
        "when_utc": "1231315",#<== not accepteable parameter
        }
    
    with pytest.raises(MsgBuilderError):
        build_goflat_order_request_msg(
            account_id = 0,
            request_id = 0,
            when_utc_timestamp = datetime.now(timezone.utc),
            **notaccept_input
            )

# - check_order_specific_essential_fields         
def test_check_order_specific_essential_fields_LMT_fail_null()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "scale_factor": 1.0
        #"limit_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **null_input)


def test_check_order_specific_essential_fields_STP_fail_null()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STP, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "scale_factor": 1.0
        #"stop_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0, 
            **null_input)
        
def test_check_order_specific_essential_fields_STL_missing_both_limit_stop_prices_fail()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STL, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "scale_factor": 1.0
        #"limit_price": 1000, <-- missing limit price
        #"stop_price": 1000, <-- missing stop price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **null_input
            )
        
def test_check_order_specific_essential_fields_STL_missing_both_limit_prices_fail()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STL, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        #"limit_price": 1000, <-- missing limit price
        "stop_price": 1000, 
        "scale_factor": 1.0
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **null_input
            )
        
def test_check_order_specific_essential_fields_STL_missing_both_stop_prices_fail()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.STL, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000,
        "scale_factor": 1.0
        #"stop_price": 1000,  <-- missing limit price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **null_input
            )        

def test_check_order_specific_essential_fields_GTD_fail_null()->None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTD, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000, 
        "scale_factor": 1.0
        #"good_thru_date": 10, <-- missing good_thru_date price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **null_input
            )       
        
def test_check_order_specific_essential_fields_Trail_fail_null()-> None:
    null_input = {
        #"symbol_name": "CLEV25",
        "cl_order_id": "1231314",
        "order_type": OrderType.LMT, 
        "duration": Duration.GTC, 
        "side": Side.BUY,
        #"qty_significant": 2,
        #"qty_exponent": 0, 
        "qty": 2,
        "is_manual": False,
        "limit_price": 1000, 
        "exec_instructions": ExecInstruction.TRAIL,
        "scale_factor": 1.0
        #"trail_offset": 10, <-- missing trail_offset price
        }
    
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id = 0, 
            request_id = 0, 
            contract_id = 0,
            **null_input
            )
        
def test_stl_missing_only_stop_price_raises():
    # STL with limit_price present but stop_price absent
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.STL,
            duration=Duration.DAY, side=Side.BUY,
            qty = 1,
            is_manual=False,
            limit_price = 10,
            scale_factor= 1.0
            #stop_price = 11 <--- missing
            
            )
        
# ---- Value validation tests ----
def test_qty_significant_zero_raises():
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.DAY, side=Side.BUY,
            qty=0,   # <-- zero
            scale_factor= 1,
            is_manual=False)

def test_qty_significant_negative_raises():
    # same but qty_significant=-1
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.DAY, 
            side=Side.BUY,
            scale_factor= 1.0,
            qty=-1,   # <-- negative
            is_manual=False)
        
def test_limit_price_zero_raises():
    # LMT order with limit_price=0
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.LMT,
            duration=Duration.DAY, side=Side.BUY,
            qty=1,
            scale_factor= 1.0,
            is_manual=False,
            limit_price = 0 # <---
            )
        
def test_limit_price_negative_raises():
    # LMT order with limit_price=-100
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.LMT,
            duration=Duration.DAY, side=Side.BUY,
            qty=1,
            scale_factor= 1.0,
            is_manual=False,
            limit_price = -100 # <---
            )
        
def test_stop_price_zero_raises():
    # STP order with stop_price=0
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.STP,
            duration=Duration.DAY, side=Side.BUY,
            qty=1,
            scale_factor= 1.0,
            is_manual=False,
            stop_price = 0 # <--- no zero
            )
        
def test_qty_exponent_out_of_range_raises():
    # qty_exponent=21 (above upper limit)
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.STP,
            duration=Duration.DAY, side=Side.BUY,
            qty=1,
            scale_factor= 1.0,
            is_manual=False,
            stop_price = 0 # <--- no zero
            )
        
def test_qty_exponent_boundary_invalid():
    # qty_exponent=20 should pass
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.DAY, side=Side.BUY,
            scale_factor= 1.0,
            qty = 1000000,# <--- exceed boundary
            is_manual=False,
            )
        
# ---- contradiction tests ----
def test_mkt_with_limit_price_raises():
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.DAY, side=Side.BUY,
            scale_factor= 1.0,
            qty = 1,
            is_manual=False,
            limit_price=1000 # <--- contradiction
            )
        
def test_mkt_with_stop_price_raises():
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.DAY, side=Side.BUY,
            scale_factor= 1.0,
            qty = 1,
            is_manual=False,
            stop_price=1000 # <--- contradiction
            )

def test_fok_with_good_thru_date_raises():
    with pytest.raises(MsgBuilderError):
        build_new_order_request_msg(
            account_id=0, request_id=0, contract_id=0,
            cl_order_id="123", order_type=OrderType.MKT,
            duration=Duration.FOK, side=Side.BUY,
            qty = 1,
            scale_factor= 1.0,
            is_manual=False,
            good_thru_date = 20251231 # <--- contradiction
            )
