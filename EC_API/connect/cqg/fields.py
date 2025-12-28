#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 22:38:58 2025

@author: dexter
"""
from typing import Union

LOGON_REQUIRED_FIELDS = {
    'user_name': ('user_name', str, str),
    'password': ('password', str, str),
    'client_app_id': ('client_app_id', str, str), 
    'client_version': ('client_version', str, str),
    'protocol_version_major': ('protocol_version_major', int, int),
    'protocol_version_minor': ('protocol_version_minor', int, int), 
    'drop_concurrent_session': ('drop_concurrent_session', bool, bool),
    'private_label': ('private_label', str, str),
    }

LOGON_OPTIONAL_FIELDS = {}

LOGOFF_REQUIRED_FIELDS = {
    'txt_msg': ('txt_msg', str, str)
    }

LOGOFF_OPTIONAL_FIELDS = {
    }

RESTORE_REQUIRED_FIELDS = {
    'client_app_id': ('client_app_id', str, str), 
    'protocol_version_major': ('protocol_version_major', int, int), 
    'protocol_version_minor': ('protocol_version_minor', int, int),
    'session_token': ('session_token', str, str),
    }

PING_REQUIRED_FIELDS = {
    }

RESOLVE_SYM_REQUIRED_FIELDS = {
    'symbol_name': ('symbol_name', str, str), 
    'request_id': ('request_id', int, int), 
    'subscribe': ('subscribe', Union[bool, None], None), 
    }