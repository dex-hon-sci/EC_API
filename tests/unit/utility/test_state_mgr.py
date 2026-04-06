#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 22:08:40 2026

@author: dexter
"""
from enum import Enum
import pytest
from EC_API.utility.state_mgr import StateMgr
from EC_API.exceptions import (
    InvalidCurrentStateError,
    InvalidNextStateError,
    StartStateError
    )

class S(Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    
SMALL_MAP = {
    S.A: [S.B],
    S.B: [S.A,S.C],
    S.C: [S.D],
    S.D: []
    }

def test_init_valid_start() -> None:
    SM = StateMgr(SMALL_MAP, start = S.A, cur = S.A)
    assert SM.start == S.A
    assert SM.finalised is False

def test_init_valid_allowed_starts() -> None:
    SM = StateMgr(SMALL_MAP, start=S.B, cur = S.B, allowed_starts=[S.A, S.B])
    assert SM.start == S.B
    
def test_init_allowed_starts_rejected() -> None:
    with pytest.raises(StartStateError):
        StateMgr(SMALL_MAP, start=S.C, cur=S.A, allowed_starts=[S.A, S.B])
        
# -- happy path transition_to
def test_transition_to_valid() -> None:
    SM = StateMgr(SMALL_MAP, start=S.A, cur=S.A)
    assert SM.transition_to(S.B) is True
    assert SM.cur == S.B

def test_transition_to_multi_steps_valid() -> None:
    SM = StateMgr(SMALL_MAP, start=S.A, cur = S.A)
    assert SM.transition_to(S.B) is True
    assert SM.transition_to(S.C) is True
    assert SM.cur == S.C

def test_transition_to_set_finalised() -> None:
    SM = StateMgr(SMALL_MAP, start=S.A, cur=S.A)
    SM.transition_to(S.B)
    SM.transition_to(S.C)
    SM.transition_to(S.D)
    assert SM.cur == S.D
    assert SM.finalised is True 


# ---- transition_to — happy path -----------------------------------------
def test_transition_to_valid_returns_true():
    sm = StateMgr(SMALL_MAP, start=S.A)
    assert sm.transition_to(S.B) is True

def test_transition_to_multiple_valid_steps():
    sm = StateMgr(SMALL_MAP, start=S.A)
    assert sm.transition_to(S.B) is True
    assert sm.transition_to(S.C) is True

def test_transition_to_to_terminal_sets_finalised():
    sm = StateMgr(SMALL_MAP, start=S.A)
    sm.transition_to(S.B)
    sm.transition_to(S.C)
    sm.transition_to(S.D)
    assert sm.finalised is True

def test_transition_to_after_finalised_returns_false():
    sm = StateMgr(SMALL_MAP, start=S.A)
    sm.transition_to(S.B)
    sm.transition_to(S.C)
    sm.transition_to(S.D)
    assert sm.transition_to(S.A) is False

def test_transition_to_non_terminal_does_not_finalise():
    sm = StateMgr(SMALL_MAP, start=S.A)
    sm.transition_to(S.B)
    assert sm.finalised is False

# ---- transition_to — error cases ----------------------------------------
def test_transition_to_unknown_cur_state_raises():
    # S.D is terminal — not valid as cur_state
    partial_map = {S.A: [S.B], S.B: [S.A]}
    with pytest.raises(InvalidCurrentStateError):
        StateMgr(partial_map, start=S.A, cur=S.D)

def test_transition_to_next_state_not_in_map_raises():
    partial_map = {S.A: [S.B], S.B: [S.A]}
    sm = StateMgr(partial_map, start=S.A)
    with pytest.raises(InvalidNextStateError):
        sm.transition_to(S.D)  # S.D not a key in map

def test_transition_to_disallowed_next_state_raises():
    # S.B → S.D is not listed under S.B's allowed transition_tos
    sm = StateMgr(SMALL_MAP, start=S.A)
    with pytest.raises(InvalidNextStateError):
        sm.transition_to(S.D)


