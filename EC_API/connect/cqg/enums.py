#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 07:30:04 2025

@author: dexter
"""


from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LOR
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LOff
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as Restore

LOGON_RESULT_STATUS_ENUMS_BOOL = {
    "Accept": [LOR.ResultCode.RESULT_CODE_SUCCESS] ,
    "Reject": [LOR.ResultCode.RESULT_CODE_FAILURE,
              LOR.ResultCode.RESULT_CODE_NO_ONETIME_PASSWORD,
              LOR.ResultCode.RESULT_CODE_PASSWORD_EXPIRED,
              LOR.ResultCode.RESULT_CODE_CONCURRENT_SESSION,
              LOR.ResultCode.RESULT_CODE_REDIRECTED,
              LOR.ResultCode.RESULT_CODE_ROUTINE_ERROR,
              LOR.ResultCode.RESULT_CODE_ACCESS_TOKEN_EXPIRED
              ]
    }

LOGGEDOFF_REASON_ENUMS_BOOL = {
    "Accept": [LOff.LogoffReason.LOGOFF_REASON_BY_REQUEST,
               LOff.LogoffReason.LOGOFF_REASON_REDIRECTED,
               LOff.LogoffReason.LOGOFF_REASON_FORCED,
               LOff.LogoffReason.LOGOFF_REASON_REASSIGNED
               ],
    "Reject": []
    }

RESTORE_STATUS_ENUMS_BOOL = {
    "Accept": [Restore.ResultCode.RESULT_CODE_SUCCESS],
    "Reject": [Restore.ResultCode.RESULT_CODE_FAILURE,
               Restore.ResultCode.RESULT_CODE_UNKNOWN_SESSION,
               Restore.ResultCode.RESULT_CODE_ACCESS_DENIED,
               Restore.ResultCode.RESULT_CODE_INVALID_PARAMS]
    }
