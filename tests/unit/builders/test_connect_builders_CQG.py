#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 18:41:33 2025

@author: dexter
"""
import pytest
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
from EC_API.exceptions import MsgBuilderError

# --- Happy Path
def test_build_logon_msg_valid() -> None:
    msg = build_logon_msg(
        'user_name', 'password',
        client_app_id = 'WebApiTest-unit-test', 
        client_version = 'python-client-test-2-240-unit-test',
        protocol_version_major = 303,
        protocol_version_minor = 240,
        drop_concurrent_session = False,
        private_label = 'private-label-unit-test',
        session_settings = 0
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
    msg = build_ping_msg('Hello', ping_utc_time=10)
    
    assert type(msg.ping) == Ping
    assert msg.ping.token == 'Hello'
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
    
# --- Sad Path

# --- build_logon_msg ---

def test_build_logon_msg_user_name_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name=123, password='password')

def test_build_logon_msg_password_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password=123)

def test_build_logon_msg_client_app_id_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        client_app_id=999)

def test_build_logon_msg_client_version_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        client_version=999)

def test_build_logon_msg_protocol_version_major_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        protocol_version_major='2')

def test_build_logon_msg_protocol_version_minor_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        protocol_version_minor='240')

def test_build_logon_msg_drop_concurrent_session_wrong_type() -> None:
    # int is not bool — bool subclasses int but not vice versa
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        drop_concurrent_session=1)

def test_build_logon_msg_private_label_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logon_msg(user_name='user', password='pass',
                        private_label=123)


# --- build_logoff_msg ---

def test_build_logoff_msg_txt_msg_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_logoff_msg(txt_msg=123)


# --- build_restore_msg ---

def test_build_restore_msg_client_app_id_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_restore_msg(client_app_id=999,
                          protocol_version_major=2,
                          protocol_version_minor=240,
                          session_token='token')

def test_build_restore_msg_protocol_version_major_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_restore_msg(client_app_id='app',
                          protocol_version_major='2',
                          protocol_version_minor=240,
                          session_token='token')

def test_build_restore_msg_protocol_version_minor_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_restore_msg(client_app_id='app',
                          protocol_version_major=2,
                          protocol_version_minor='240',
                          session_token='token')

def test_build_restore_msg_session_token_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_restore_msg(client_app_id='app',
                          protocol_version_major=2,
                          protocol_version_minor=240,
                          session_token=12345)


# --- build_ping_msg ---

def test_build_ping_msg_token_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_ping_msg(token=999, ping_utc_time=10)

def test_build_ping_msg_ping_utc_time_wrong_type_str() -> None:
    with pytest.raises(MsgBuilderError):
        build_ping_msg(token='hello', ping_utc_time='10')

def test_build_ping_msg_ping_utc_time_wrong_type_float() -> None:
    with pytest.raises(MsgBuilderError):
        build_ping_msg(token='hello', ping_utc_time=10.0)


# --- build_resolve_symbol_msg ---

def test_build_resolve_symbol_msg_symbol_name_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_resolve_symbol_msg(symbol_name=12345, request_id=1)

def test_build_resolve_symbol_msg_request_id_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_resolve_symbol_msg(symbol_name='CLEV25', request_id='1')

def test_build_resolve_symbol_msg_subscribe_wrong_type() -> None:
    with pytest.raises(MsgBuilderError):
        build_resolve_symbol_msg(symbol_name='CLEV25', request_id=1,
                                 subscribe='yes')
   