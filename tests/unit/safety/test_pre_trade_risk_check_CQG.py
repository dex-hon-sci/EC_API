import pytest
from pathlib import Path
from EC_API.protocol.cqg.risk_field_mappings import CQG_RISK_FIELD_MAP
from EC_API.payload.safety import PreTradeRiskCheck
from EC_API.exceptions import MissingVendorError

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
TEST_RISK_CONFIG = FIXTURES_DIR / "test_pretrade_risk_check.toml"

def test_init_field_map_success()-> None:
    PTRC = PreTradeRiskCheck('cqg')
    assert PTRC.field_map == CQG_RISK_FIELD_MAP
    
def test_init_field_map_fail() -> None:
    with pytest.raises(MissingVendorError):
        PreTradeRiskCheck('fake_vendor')
        
def test_load_static_risk_file() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
        
    assert PTRC._aliases['A'] == "Asset_A"
    assert PTRC._aliases['A14'] == "Asset_A"
    assert PTRC._aliases['Asset_A'] == "Asset_A"
    assert PTRC._aliases['CLEV25'] == "CL_GENERIC"

    assert PTRC.global_limits['qty_max'] == 10
    assert isinstance(PTRC.global_limits['qty_max'],int)
    
    assert PTRC.symbol_limits['Asset_A']['qty_max'] == 11
    assert PTRC.symbol_limits['Asset_A']['price_max'] == 201.0
    assert PTRC.symbol_limits['Asset_A']['price_min'] == 51.0
    assert PTRC.symbol_limits['Asset_A']['stop_price_max'] == 211.0
    assert isinstance(PTRC.symbol_limits['Asset_A']['qty_max'], int)
    assert isinstance(PTRC.symbol_limits['Asset_A']['price_max'], float)
    assert isinstance(PTRC.symbol_limits['Asset_A']['price_min'], float)
    assert isinstance(PTRC.symbol_limits['Asset_A']['stop_price_max'], float)

    assert PTRC.symbol_limits['CL_GENERIC']['qty_max'] == 12
    assert PTRC.symbol_limits['CL_GENERIC']['price_max'] == 202.0
    assert PTRC.symbol_limits['CL_GENERIC']['price_min'] == 52.0
    assert PTRC.symbol_limits['CL_GENERIC']['stop_price_max'] == 212.0
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['qty_max'], int)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['price_max'], float)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['price_min'], float)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['stop_price_max'], float)

def test_reload_static_risk_file() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.reload(TEST_RISK_CONFIG)
        
    assert PTRC._aliases['A'] == "Asset_A"
    assert PTRC._aliases['A14'] == "Asset_A"
    assert PTRC._aliases['Asset_A'] == "Asset_A"
    assert PTRC._aliases['CLEV25'] == "CL_GENERIC"

    assert PTRC.global_limits['qty_max'] == 10
    assert isinstance(PTRC.global_limits['qty_max'],int)
    
    assert PTRC.symbol_limits['Asset_A']['qty_max'] == 11
    assert PTRC.symbol_limits['Asset_A']['price_max'] == 201.0
    assert PTRC.symbol_limits['Asset_A']['price_min'] == 51.0
    assert PTRC.symbol_limits['Asset_A']['stop_price_max'] == 211.0
    assert isinstance(PTRC.symbol_limits['Asset_A']['qty_max'], int)
    assert isinstance(PTRC.symbol_limits['Asset_A']['price_max'], float)
    assert isinstance(PTRC.symbol_limits['Asset_A']['price_min'], float)
    assert isinstance(PTRC.symbol_limits['Asset_A']['stop_price_max'], float)

    assert PTRC.symbol_limits['CL_GENERIC']['qty_max'] == 12
    assert PTRC.symbol_limits['CL_GENERIC']['price_max'] == 202.0
    assert PTRC.symbol_limits['CL_GENERIC']['price_min'] == 52.0
    assert PTRC.symbol_limits['CL_GENERIC']['stop_price_max'] == 212.0
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['qty_max'], int)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['price_max'], float)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['price_min'], float)
    assert isinstance(PTRC.symbol_limits['CL_GENERIC']['stop_price_max'], float)
    
def test_update_success() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    
    new_para = {
        'qty_max': 0,
        'price_max': 0,
        'price_min': 0,
        'stop_price_min': 0
        }
    
    PTRC.update("A", new_para)
    
    assert PTRC.symbol_limits['Asset_A']['qty_max'] == 0
    assert PTRC.symbol_limits['Asset_A']['price_max'] == 0
    assert PTRC.symbol_limits['Asset_A']['price_min'] == 0
    assert PTRC.symbol_limits['Asset_A']['stop_price_min'] == 0
    
def test_update_fail_invalid_para() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    with pytest.raises(ValueError):
        PTRC.update("A", "A") # Incorrect para type
        
def test_update_fail_invalid_alias() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    with pytest.raises(ValueError):
        PTRC.update("B", dict()) # 'B' Not in alias

def test_static_validate_success() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    
    order_info = {
        'symbol_name': 'A14',
        'qty': 3,
        'limit_price': 100,
        'is_manual': True 
        }
    # If return None, it passes every tests
    assert PTRC.static_validate(order_info) is None
    
def test_static_validate_fail_no_symbol_name() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        #'symbol_name': 'A14', #<--missing symbol_name
        'qty': 3.0,
        'limit_price': 100
        }
    with pytest.raises(KeyError):
        PTRC.static_validate(order_info)
        
    
def test_static_validate_fail_symbol_name_not_in_checklist() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'B14', #<--missing symbol_name
        'qty': 3.0,
        'limit_price': 100
        }
    with pytest.raises(KeyError):
        PTRC.static_validate(order_info)       
        
def test_static_validate_fail_exceed_limit_price() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 3.0,
        'limit_price': 300 #<---limit price exceed
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)

def test_static_validate_fail_below_limit_price() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 3.0,
        'limit_price': 30 #<---limit price below
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)
        
def test_static_validate_fail_exceed_stop_price() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 3.0,
        'stop_price': 215 #<---limit price exceed
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)

def test_static_validate_fail_below_stop_price() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 3.0,
        'stop_price': 100 #<---limit price below
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)
    
        
def test_static_validate_global_exceed_limit_qty() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 100, #<---global limit qty exceeded
        'stop_price': 200 
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)

def test_static_validate_global_below_limit_qty() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        'symbol_name': 'A14',
        'qty': 1, #<---global limit qty below
        'stop_price': 200 
        }
    with pytest.raises(ValueError):
        PTRC.static_validate(order_info)
        
# Lines 67-69: unknown key in global_limits not in field_map
def test_static_validate_unknown_global_field_raises() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    PTRC.global_limits['unknown_param_max'] = 999  # inject unknown key
    order_info = {
        "symbol_name": "A",
        "qty_significant": 5,
    }
    with pytest.raises(KeyError):
        PTRC.static_validate(order_info)

# Line 72: field in global_limits but absent from order_info -> continue, no error
def test_static_validate_global_field_absent_in_order_skips() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        "symbol_name": "A",
        # qty deliberately absent — global qty_max/qty_min should be skipped
        }
    PTRC.static_validate(order_info)  # should not raise

# Lines 97-99: unknown key in symbol_limits not in field_map
# CL_GENERIC already has duration_max in the test TOML which is not in
CQG_RISK_FIELD_MAP
def test_static_validate_unknown_symbol_field_raises() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    order_info = {
        "symbol_name": "CLEV25",
        "qty_significant": 5,
    }
    with pytest.raises(KeyError):
        PTRC.static_validate(order_info)

# Lines 50-52: alias maps to profile not in symbol_limits (defensive guard)
def test_update_alias_points_to_missing_profile_raises() -> None:
    PTRC = PreTradeRiskCheck('cqg')
    PTRC.load(TEST_RISK_CONFIG)
    PTRC._aliases['ghost'] = 'NONEXISTENT_PROFILE'  # alias exists, profile doesn't
    with pytest.raises(ValueError):
        PTRC.update('ghost', {'qty_max': 5})
