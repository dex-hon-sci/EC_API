#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 22:38:58 2025

@author: dexter
"""
from typing import Union

LOGON_REQUEST_REQUIRED_FIELDS = {
    'user_name': ('user_name', str, str),
    'password': ('password', str, str),
    'client_app_id': ('client_app_id', str, str), 
    'client_version': ('client_version', str, str),
    'protocol_version_major': ('protocol_version_major', int, int),
    'protocol_version_minor': ('protocol_version_minor', int, int), 
    'drop_concurrent_session': ('drop_concurrent_session', bool, bool),
    'private_label': ('private_label', str, str),
    }

LOGON_REQUEST_OPTIONAL_FIELDS = {}

LOGOFF_REQUEST_REQUIRED_FIELDS = {
    'txt_msg': ('txt_msg', str, str)
    }

LOGOFF_REQUEST_OPTIONAL_FIELDS = {
    }

RESTORE_REQUEST_REQUIRED_FIELDS = {
    'client_app_id': ('client_app_id', str, str), 
    'protocol_version_major': ('protocol_version_major', int, int), 
    'protocol_version_minor': ('protocol_version_minor', int, int),
    'session_token': ('session_token', str, str),
    }

PING_REQUEST_REQUIRED_FIELDS = {
    'ping_utc_time': ('ping_utc_time', int, int)
    }

RESOLVE_SYM_REQUEST_REQUIRED_FIELDS = {
    'symbol_name': ('symbol_name', str, str), 
    'request_id': ('request_id', int, int), 
    'subscribe': ('subscribe', Union[bool, None], None), 
    }