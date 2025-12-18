#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:41:33 2025

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.ext.WebAPI.user_session_2_pb2 import Logon, Logoff
from EC_API.connect.cqg.builders import (
    build_logon_msg, build_logoff_msg,
    build_restore_msg, build_ping_msg,
    build_pong_msg, build_resolve_symbol_msg
    )

def test_build_logon_msg() -> None:
    msg = build_logon_msg(
        'user_name', 'password',
        client_app_id = 'WebApiTest-unit-test', 
        client_version = 'python-client-test-2-240-unit-test',
        protocol_version_major = '',
        protocol_version_minor = '',
        drop_concurrent_session = '',
        private_label = 'private-label-unit-test'
        )

    assert type(msg) == ClientMsg
    assert type(msg.logon) == Logon
    assert msg.logon.user_name == 'user_name'
    assert msg.logon.password == 'password'
    assert msg.logon.client_app_id == 'WebApiTest-unit-test'
    assert msg.logon.client_version == 'python-client-test-2-240-unit-test'
    assert msg.logon.protocol_version_major == ''
    assert msg.logon.protocol_version_minor == ''
    assert msg.logon.drop_concurrent_session == ''
    assert msg.logon.private_label == 'private-label-unit-test'

def test_build_logoff_msg() -> None:
    msg = build_logoff_msg(
        txt_msg="Test_logoff"
        )
    assert type(msg.logoff) == Logoff
    assert msg.logoff == "Test_logoff"
    
def test_build_restore_msg() -> None:
    pass

def test_build_ping_msg() -> None:
    pass

def test_build_resolve_symbol_msg() -> None:
    pass