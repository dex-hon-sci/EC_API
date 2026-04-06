#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 03:39:31 2026

@author: dexter
"""
from EC_API.connect.enums import ConnectionState, CONNECT_STATES_LIFECYCLE
from EC_API.utility.state_mgr import StateMgr

# ---- ConnectionState integration -------------------------------------
def test_connect_lifecycle_happy_path():
    sm = StateMgr(
        CONNECT_STATES_LIFECYCLE,
        start=ConnectionState.UNKNOWN,
        allowed_starts=[ConnectionState.UNKNOWN]
    )
    assert sm.transition_to(ConnectionState.CONNECTING) is True
    assert sm.transition_to(ConnectionState.CONNECTED_DEFAULT) is True
    assert sm.transition_to(ConnectionState.CONNECTED_LOGON) is True

def test_connect_lifecycle_closed_is_terminal():
    sm = StateMgr(CONNECT_STATES_LIFECYCLE, start=ConnectionState.UNKNOWN)
    sm.transition_to(ConnectionState.CONNECTING)
    sm.transition_to(ConnectionState.CONNECTED_DEFAULT)
    sm.transition_to(ConnectionState.CONNECTED_LOGON)
    sm.transition_to(ConnectionState.CONNECTED_LOGOFF)
    sm.transition_to(ConnectionState.DISCONNECTED)
    sm.transition_to(ConnectionState.CLOSING)
    sm.transition_to(ConnectionState.CLOSED)
    assert sm.finalised is True
