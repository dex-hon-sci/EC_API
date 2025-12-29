#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 23:19:07 2025

@author: dexter
"""
from EC_API.connect.enums import ConnectionState
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LOR
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LOff
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as Restore



CONN_MSG_RESULTCODE_CQG2INT = { # Move these two parsers
    # Failed Logon attempts but connection still intact
    LOR.ResultCode.RESULT_CODE_FAILURE: ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_NO_ONETIME_PASSWORD: ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_PASSWORD_EXPIRED:ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_CONCURRENT_SESSION:ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_REDIRECTED: ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_ROUTINE_ERROR: ConnectionState.CONNECTED_DEFAULT,
    LOR.ResultCode.RESULT_CODE_ACCESS_TOKEN_EXPIRED: ConnectionState.CONNECTED_DEFAULT,
    Restore.ResultCode.RESULT_CODE_FAILURE: ConnectionState.CONNECTED_DEFAULT,
    Restore.ResultCode.RESULT_CODE_UNKNOWN_SESSION: ConnectionState.CONNECTED_DEFAULT,
    Restore.ResultCode.RESULT_CODE_ACCESS_DENIED: ConnectionState.CONNECTED_DEFAULT,
    Restore.ResultCode.RESULT_CODE_INVALID_PARAMS: ConnectionState.CONNECTED_DEFAULT,
    # Successful Logon/Logoff enum
    LOR.ResultCode.RESULT_CODE_SUCCESS: ConnectionState.CONNECTED_LOGON,
    Restore.ResultCode.RESULT_CODE_SUCCESS: ConnectionState.CONNECTED_LOGON,
    LOff.LogoffReason.LOGOFF_REASON_BY_REQUEST: ConnectionState.CONNECTED_LOGOFF,
    LOff.LogoffReason.LOGOFF_REASON_REDIRECTED: ConnectionState.CONNECTED_LOGOFF,
    LOff.LogoffReason.LOGOFF_REASON_FORCED: ConnectionState.CONNECTED_LOGOFF,
    LOff.LogoffReason.LOGOFF_REASON_REASSIGNED: ConnectionState.CONNECTED_LOGOFF,    
    }