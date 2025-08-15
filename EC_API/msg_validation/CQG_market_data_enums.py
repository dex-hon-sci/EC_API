#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 11:57:10 2025

@author: dexter
"""

from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscriptionStatus as MDSS

MARKETDATA_SUB_STATUS_ENUMS_BOOL = {
    "Accept": [MDSS.StatusCode.STATUS_CODE_SUCCESS,
               ],
    "Reject": [MDSS.StatusCode.STATUS_CODE_DISCONNECTED,
               MDSS.StatusCode.STATUS_CODE_FAILURE,
               MDSS.StatusCode.STATUS_CODE_INVALID_PARAMS,
               MDSS.StatusCode.STATUS_CODE_ACCESS_DENIED,
               MDSS.StatusCode.STATUS_CODE_DELETED,
               MDSS.StatusCode.STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION,
               MDSS.StatusCode.STATUS_CODE_CONTRIBUTOR_REQUIRED,
               MDSS.StatusCode.STATUS_CODE_SUBSCRIPTION_RATE_LIMIT_VIOLATION,
               MDSS.StatusCode.STATUS_CODE_NOT_SUPPORTED,
               ]
    }

