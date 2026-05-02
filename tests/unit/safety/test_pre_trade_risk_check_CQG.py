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



        

