#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:41:33 2025

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import (
    ClientMsg, InformationRequest,
    )
from EC_API.ext.WebAPI.user_session_2_pb2 import ( 
    Logon, Logoff, 
    RestoreOrJoinSession,
    Ping
    )
from EC_API.connect.cqg.builders import (
    build_logon_msg, build_logoff_msg,
    build_restore_msg, build_ping_msg,
    build_resolve_symbol_msg
    )

def test_build_logon_msg_valid() -> None:
    msg = build_logon_msg(
        'user_name', 'password',
        client_app_id = 'WebApiTest-unit-test', 
        client_version = 'python-client-test-2-240-unit-test',
        protocol_version_major = 303,
        protocol_version_minor = 240,
        drop_concurrent_session = False,
        private_label = 'private-label-unit-test'
        )

    assert type(msg) == ClientMsg
    assert type(msg.logon) == Logon
    assert msg.logon.user_name == 'user_name'
    assert msg.logon.password == 'password'
    assert msg.logon.client_app_id == 'WebApiTest-unit-test'
    assert msg.logon.client_version == 'python-client-test-2-240-unit-test'
    assert msg.logon.protocol_version_major == 303
    assert msg.logon.protocol_version_minor == 240
    assert msg.logon.drop_concurrent_session == False
    assert msg.logon.private_label == 'private-label-unit-test'

def test_build_logoff_msg_valid() -> None:
    msg = build_logoff_msg(
        txt_msg="Test_logoff"
        )
    assert type(msg.logoff) == Logoff
    assert msg.logoff.text_message == "Test_logoff"
    
def test_build_restore_msg_valid() -> None:
    msg = build_restore_msg(
        client_app_id ='WebApiTest-unit-test', 
        protocol_version_major = 303, 
        protocol_version_minor = 240,
        session_token = "ABCDEFG",
        )
    
    assert type(msg.restore_or_join_session) == RestoreOrJoinSession
    restor_msg = msg.restore_or_join_session
    assert restor_msg.client_app_id =='WebApiTest-unit-test'
    assert restor_msg.protocol_version_major == 303
    assert restor_msg.protocol_version_minor == 240
    assert restor_msg.session_token == "ABCDEFG"

def test_build_ping_msg_valid() -> None:
    msg = build_ping_msg(ping_utc_time=10)
    
    assert type(msg.ping) == Ping
    assert msg.ping.ping_utc_time == 10

def test_build_resolve_symbol_msg_valid() -> None:
    msg = build_resolve_symbol_msg(symbol_name="CLEV25",
                                   request_id= 101,
                                   subscribe=True,
                                   instrument_group_request="CLE")
    
    assert type(msg.information_requests[0]) == InformationRequest
    assert msg.information_requests[0].symbol_resolution_request.symbol == "CLEV25"    
    assert msg.information_requests[0].id == 101
    assert msg.information_requests[0].subscribe == True
    instrument_gp_request = msg.information_requests[0].instrument_group_request
    assert instrument_gp_request.instrument_group_id == "CLE"
    