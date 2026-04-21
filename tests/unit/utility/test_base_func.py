import pytest
import pickle
import tempfile
import os
from decimal import Decimal
from unittest.mock import MagicMock
from EC_API.utility.base import (
    random_string,
    foo,
    to_significand_sint64_exponent_sint32,
    time_it,
    save_csv,
    pickle_save,
    load_pkl,
)


# --- random_string ---

def test_random_string_default_length():
    result = random_string()
    assert len(result) == 16

def test_random_string_custom_length():
    result = random_string(8)
    assert len(result) == 8

def test_random_string_only_digits():
    result = random_string(100)
    assert result.isdigit()

def test_random_string_zero_length():
    assert random_string(0) == ""


# --- foo ---

def test_foo_positive():
    sig, exp = foo(Decimal("1.25"))
    assert sig == 125
    assert exp == -2

def test_foo_negative():
    sig, exp = foo(Decimal("-1.25"))
    assert sig == -125
    assert exp == -2

def test_foo_integer():
    sig, exp = foo(Decimal("100"))
    assert sig == 1
    assert exp == 2

def test_foo_trailing_zeros_normalized():
    sig, exp = foo(Decimal("1.2500"))
    assert sig == 125
    assert exp == -2


# --- to_significand_sint64_exponent_sint32 ---

def test_to_sig_exp_integer():
    sig, exp = to_significand_sint64_exponent_sint32(100)
    assert sig == 1
    assert exp == 2

def test_to_sig_exp_float():
    sig, exp = to_significand_sint64_exponent_sint32(1.25)
    assert sig == 125
    assert exp == -2

def test_to_sig_exp_negative():
    sig, exp = to_significand_sint64_exponent_sint32(-1.25)
    assert sig == -125
    assert exp == -2

def test_to_sig_exp_zero():
    sig, exp = to_significand_sint64_exponent_sint32(0)
    assert sig == 0

def test_to_sig_exp_reconstructs_value():
    n = 12345.678
    sig, exp = to_significand_sint64_exponent_sint32(n)
    assert sig * (10 ** exp) == pytest.approx(n)

def test_to_sig_exp_overflow_significand():
    huge = 2**63  # exceeds sint64
    with pytest.raises(ValueError, match="sint64"):
        to_significand_sint64_exponent_sint32(huge)


# --- time_it ---

def test_time_it_returns_result(capsys):
    @time_it
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5

def test_time_it_prints_timing(capsys):
    @time_it
    def noop():
        pass

    noop()
    captured = capsys.readouterr()
    assert "noop" in captured.out
    assert "seconds" in captured.out


# --- save_csv ---

def test_save_csv_saves_file(tmp_path):
    outfile = str(tmp_path / "out.csv")
    mock_df = MagicMock()

    @save_csv(outfile, save_or_not=True)
    def get_data():
        return mock_df

    result = get_data()
    mock_df.to_csv.assert_called_once_with(outfile, index=False)
    assert result is mock_df

def test_save_csv_skip_save(tmp_path):
    outfile = str(tmp_path / "out.csv")
    mock_df = MagicMock()

    @save_csv(outfile, save_or_not=False)
    def get_data():
        return mock_df

    result = get_data()
    mock_df.to_csv.assert_not_called()
    assert result is mock_df


# --- pickle_save and load_pkl ---

def test_pickle_save_and_load(tmp_path):
    outfile = str(tmp_path / "data.pkl")

    @pickle_save(outfile, save_or_not=True)
    def get_data():
        return {"key": 42}

    result = get_data()
    assert result == {"key": 42}

    loaded = load_pkl(outfile)
    assert loaded == {"key": 42}

def test_pickle_save_skip(tmp_path):
    outfile = str(tmp_path / "data.pkl")

    @pickle_save(outfile, save_or_not=False)
    def get_data():
        return [1, 2, 3]

    result = get_data()
    assert result == [1, 2, 3]
    assert not os.path.exists(outfile)