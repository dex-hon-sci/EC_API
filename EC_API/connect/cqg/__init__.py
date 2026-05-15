#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:22:55 2025

@author: dexter
"""

from .base import ConnectCQG
from .enum_mapping import (
    CONN_LOGON_RESCODE_CQG2INT,
    CONN_LOGOFF_RESCODE_CQG2INT,
    CONN_RESTORE_RESCODE_CQG2INT,
)
from .builders import (
    build_logon_msg,
    build_logoff_msg,
    build_restore_msg,
    build_ping_msg,
    build_resolve_symbol_msg,
)
from .parsers import (
    parse_logon_result,
    parse_restore_or_join_session_result,
    parse_logged_off,
    parse_pong,
    parse_symbol_resolution_report,
)
from .fields import (
    LOGON_REQUEST_REQUIRED_FIELDS,
    LOGON_REQUEST_OPTIONAL_FIELDS,
    LOGOFF_REQUEST_REQUIRED_FIELDS,
    LOGOFF_REQUEST_OPTIONAL_FIELDS,
    RESTORE_REQUEST_REQUIRED_FIELDS,
    PING_REQUEST_REQUIRED_FIELDS,
    RESOLVE_SYM_REQUEST_REQUIRED_FIELDS,
)

__all__ = [
    # --- base
    "ConnectCQG",
    # --- enum mapping
    "CONN_LOGON_RESCODE_CQG2INT",
    "CONN_LOGOFF_RESCODE_CQG2INT",
    "CONN_RESTORE_RESCODE_CQG2INT",
    # --- builders
    "build_logon_msg",
    "build_logoff_msg",
    "build_restore_msg",
    "build_restore_msg",
    "build_ping_msg",
    "build_resolve_symbol_msg",
    # --- parsers
    "parse_logon_result",
    "parse_restore_or_join_session_result",
    "parse_logged_off",
    "parse_pong",
    "parse_symbol_resolution_report",
    # --- fields
    "LOGON_REQUEST_REQUIRED_FIELDS",
    "LOGON_REQUEST_OPTIONAL_FIELDS",
    "LOGOFF_REQUEST_REQUIRED_FIELDS",
    "LOGOFF_REQUEST_OPTIONAL_FIELDS",
    "RESTORE_REQUEST_REQUIRED_FIELDS",
    "PING_REQUEST_REQUIRED_FIELDS",
    "RESOLVE_SYM_REQUEST_REQUIRED_FIELDS",
]
