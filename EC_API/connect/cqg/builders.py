#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 17:54:16 2025

@author: dexter
"""
import logging
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.exceptions import (
    MsgBuilderParaTypeError
    )
from EC_API.protocol.cqg.builder_util import (
    apply_optional_fields, 
    assert_input_types
    )
from EC_API.connect.cqg.fields import (
    LOGON_REQUEST_REQUIRED_FIELDS,
    LOGOFF_REQUEST_REQUIRED_FIELDS,
    RESTORE_REQUEST_REQUIRED_FIELDS,
    PING_REQUEST_REQUIRED_FIELDS,
    RESOLVE_SYM_REQUEST_REQUIRED_FIELDS
    )

logger = logging.getLogger(__name__)

def build_logon_msg(
    user_name: str,
    password: str,
    client_app_id: str ='WebApiTest', 
    client_version: str ='python-client-test-2-240',
    protocol_version_major: int = 2,
    protocol_version_minor: int = 240, 
    drop_concurrent_session: bool = False,
    private_label: str = "WebApiTest",
    **kwargs
    ) -> ClientMsg:
    
    kwargs = dict({}, **kwargs)    
    params = locals().copy()
    params.pop('kwargs')
    try:
        assert_input_types(params, LOGON_REQUEST_REQUIRED_FIELDS)
    except (KeyError, TypeError, ValueError) as e:
        msg = f"build_logon_msg invalid parameters: {str(e)}"
        logger.error(msg)
        return None

    #assert_input_types(kwargs, LOGON_OPTIONAL_FIELDS)
    
    # create a client_msg based on the protocol.
    client_msg = ClientMsg()
    
    # initialize the logon message, there are four required parameters.
    logon = client_msg.logon
    logon.user_name = user_name
    logon.password = password
    logon.client_app_id = client_app_id
    logon.client_version = client_version
    logon.protocol_version_major = protocol_version_major
    logon.protocol_version_minor = protocol_version_minor
    logon.drop_concurrent_session = drop_concurrent_session
    logon.private_label = private_label

    if 'session_settings' in kwargs:
        logon.session_settings.add(kwargs['session_settings'])
    return client_msg

def build_logoff_msg(txt_msg: str="logoff") -> ClientMsg:
    params = locals().copy()    
    try:
        assert_input_types(params, LOGOFF_REQUEST_REQUIRED_FIELDS)
    except (TypeError, KeyError, ValueError) as e:
        msg = f"build_logoff_msg invalid parameters: {str(e)}"
        logger.error(msg)
        return 
    
    # Logoff. Invoke this everytime when a connection is dropped
    client_msg = ClientMsg()
    logoff = client_msg.logoff
    logoff.text_message = txt_msg
    return client_msg
    
def build_restore_msg(
    client_app_id: str, 
    protocol_version_major: int, 
    protocol_version_minor: int,
    session_token: str,
    **kwargs
    ) -> ClientMsg:
    params = locals().copy()
    params.pop('kwargs')
    try:
        assert_input_types(params, RESTORE_REQUEST_REQUIRED_FIELDS)
    except (TypeError, KeyError, ValueError) as e:
        msg = f"build_restore_msg invalid parameters: {str(e)}"
        logger.error(msg)
        return 


    # Restore request taken from class attributes
    restore_msg = ClientMsg()
    restore_request = restore_msg.restore_or_join_session 
    restore_request.client_app_id = client_app_id
    restore_request.protocol_version_major = protocol_version_major
    restore_request.protocol_version_minor = protocol_version_minor
    restore_request.session_token = session_token
    return restore_msg

def build_ping_msg(
        token: str, 
        ping_utc_time: int
    ) -> ClientMsg | None:
    params = locals().copy()
    try:
        assert_input_types(params, PING_REQUEST_REQUIRED_FIELDS)
    except (TypeError, KeyError, ValueError) as e:
        msg = f"build_ping_msg invalid parameters: {str(e)}."
        logger.error(msg)
        return 

    client_msg = ClientMsg()
    pr = client_msg.ping
    pr.token = token
    pr.ping_utc_time = ping_utc_time
    return client_msg

def build_resolve_symbol_msg(                       
    symbol_name: str, 
    request_id: int, 
    subscribe: bool | None = None, 
    **kwargs
    ) -> ClientMsg | None:
    params = locals().copy()
    params.pop('kwargs')
    try:
        assert_input_types(params, RESOLVE_SYM_REQUEST_REQUIRED_FIELDS)
    except (TypeError, KeyError, ValueError) as e:
        msg = f"..."
        logger.error(msg)
        return

    client_msg = ClientMsg()
    information_request = client_msg.information_requests.add()
    
    # This example assume one symbol only.
    information_request.id = request_id
    if subscribe is not None:
        information_request.subscribe = subscribe
        
    information_request.symbol_resolution_request.symbol = symbol_name
    
    if 'instrument_group_request' in kwargs:
        information_request.instrument_group_request.instrument_group_id = kwargs['instrument_group_request']
         
    return client_msg
