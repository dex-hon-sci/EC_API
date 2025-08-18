#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 10:53:27 2025

@author: dexter
"""

from EC_API.ext.WebAPI.webapi_2_pb2 import InformationReport as IR

INFORMATION_REPORT_STATUS_ENUMS_BOOL = {
    "Accept": [IR.StatusCode.STATUS_CODE_SUCCESS,
               IR.StatusCode.STATUS_CODE_SUBSCRIBED,
               IR.StatusCode.STATUS_CODE_DROPPED,
               IR.StatusCode.STATUS_CODE_UPDATE
               ],
    "Reject": [IR.StatusCode.STATUS_CODE_DISCONNECTED,
               IR.StatusCode.STATUS_CODE_FAILURE,
               IR.StatusCode.STATUS_CODE_INVALID_PARAMS,
               IR.StatusCode.STATUS_CODE_NOT_FOUND,
               IR.StatusCode.STATUS_CODE_REQUEST_RATE_LIMIT_VIOLATION,
               IR.StatusCode.STATUS_CODE_ACTIVE_REQUESTS_LIMIT_VIOLATION,
               IR.StatusCode.STATUS_CODE_TOO_LARGE_RESPONSE
               ],
    "Transit": []
    }
