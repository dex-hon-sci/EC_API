import pytest
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.exceptions import (
    SymbolNotInRegistryError,
    MetaDataMissingError,
    DuplicateSymbolError,
)

SYMBOL   = "ES"
CONTRACT = 12345
METADATA = {"contract_id": CONTRACT, "currency": "USD"}

SYMBOL2   = "NQ"
CONTRACT2 = 67890
METADATA2 = {"contract_id": CONTRACT2, "currency": "USD"}


@pytest.fixture
def reg():
    return SymbolRegistry()

@pytest.fixture
def reg_with_symbol(reg):
    reg.add_symbol(SYMBOL, CONTRACT)
    return reg

@pytest.fixture
def reg_with_metadata(reg):
    reg.add_metadata(SYMBOL, METADATA)
    return reg

@pytest.fixture
def reg_registered(reg):
    reg.register(SYMBOL, METADATA)
    return reg


# ---- add_symbol -------------------------------------------------------------
def test_add_symbol_returns_true(reg):
    assert reg.add_symbol(SYMBOL, CONTRACT) is True

def test_add_symbol_stored(reg):
    reg.add_symbol(SYMBOL, CONTRACT)
    assert reg.sym_to_contract_ids[SYMBOL] == CONTRACT

def test_add_symbol_duplicate_raises(reg_with_symbol):
    with pytest.raises(DuplicateSymbolError):
        reg_with_symbol.add_symbol(SYMBOL, CONTRACT)


# ---- remove_symbol ----------------------------------------------------------
def test_remove_symbol_returns_true(reg_with_symbol):
    assert reg_with_symbol.remove_symbol(SYMBOL) is True

def test_remove_symbol_removes_entry(reg_with_symbol):
    reg_with_symbol.remove_symbol(SYMBOL)
    assert SYMBOL not in reg_with_symbol.sym_to_contract_ids

def test_remove_symbol_missing_raises(reg):
    with pytest.raises(SymbolNotInRegistryError):
        reg.remove_symbol(SYMBOL)


# ---- add_metadata -----------------------------------------------------------
def test_add_metadata_returns_true(reg):
    assert reg.add_metadata(SYMBOL, METADATA) is True

def test_add_metadata_stored(reg):
    reg.add_metadata(SYMBOL, METADATA)
    assert reg.metatdata[SYMBOL] == METADATA

def test_add_metadata_duplicate_raises(reg_with_metadata):
    with pytest.raises(DuplicateSymbolError):
        reg_with_metadata.add_metadata(SYMBOL, METADATA)


# ---- remove_metadata --------------------------------------------------------
def test_remove_metadata_returns_true(reg_with_metadata):
    assert reg_with_metadata.remove_metadata(SYMBOL) is True

def test_remove_metadata_removes_entry(reg_with_metadata):
    reg_with_metadata.remove_metadata(SYMBOL)
    assert SYMBOL not in reg_with_metadata.metatdata

def test_remove_metadata_missing_raises(reg):
    with pytest.raises(MetaDataMissingError):
        reg.remove_metadata(SYMBOL)


# ---- register ---------------------------------------------------------------
def test_register_returns_true(reg):
    assert reg.register(SYMBOL, METADATA) is True
    assert SYMBOL in reg.sym_to_contract_ids
    assert reg.sym_to_contract_ids[SYMBOL] == CONTRACT
    assert METADATA['contract_id'] == reg.metatdata[SYMBOL]['contract_id']
    assert METADATA['currency'] == reg.metatdata[SYMBOL]['currency']

def test_register_populates_contract_id(reg):
    reg.register(SYMBOL, METADATA)
    assert reg.sym_to_contract_ids[SYMBOL] == CONTRACT

def test_register_populates_metadata(reg):
    reg.register(SYMBOL, METADATA)
    assert reg.metatdata[SYMBOL] == METADATA

def test_register_duplicate_returns_false(reg_registered):
    assert reg_registered.register(SYMBOL, METADATA) is False

def test_register_multiple_symbols(reg):
    reg.register(SYMBOL, METADATA)
    reg.register(SYMBOL2, METADATA2)
    assert reg.sym_to_contract_ids[SYMBOL2] == CONTRACT2


# ---- deregister -------------------------------------------------------------
def test_deregister_returns_true(reg_registered):
    assert reg_registered.deregister(SYMBOL) is True
    

def test_deregister_removMETADATAes_contract_id(reg_registered):
    reg_registered.deregister(SYMBOL)
    assert SYMBOL not in reg_registered.sym_to_contract_ids

def test_deregister_removes_metadata(reg_registered):
    reg_registered.deregister(SYMBOL)
    assert SYMBOL not in reg_registered.metatdata

def test_deregister_missing_returns_false(reg):
    assert reg.deregister(SYMBOL) is False


# ---- get_contract_ids -------------------------------------------------------
def test_get_contract_ids_returns_correct_id(reg_registered):
    assert reg_registered.get_contract_ids(SYMBOL) == CONTRACT

def test_get_contract_ids_missing_raises(reg):
    with pytest.raises(SymbolNotInRegistryError):
        reg.get_contract_ids(SYMBOL)


# ---- get_metadata -----------------------------------------------------------
def test_get_metadata_returns_correct_metadata(reg_registered):
    assert reg_registered.get_metadata(SYMBOL) == METADATA

def test_get_metadata_missing_raises(reg):
    with pytest.raises(MetaDataMissingError):
        reg.get_metadata(SYMBOL)