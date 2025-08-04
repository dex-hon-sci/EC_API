#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 18:54:28 2025

@author: dexter
"""

from EC_API.ext.common.shared_1_pb2 import OrderStatus as OS
from EC_PAI.ext.WebAPI.trading_route_2_pb2 import TradeSubscriptionStatus as TSS
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus as GFS

TRADESUBSCRIPTIONS_STATUS_ENUMS_BOOL = {
    "Accept": [TSS.StatusCode.STATUS_CODE_SUCCESS],
    "Reject": [TSS.StatusCode.STATUS_CODE_DISCONNECTED,
               TSS.StatusCode.STATUS_CODE_FAILURE,
               TSS.StatusCode.STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION,
               TSS.StatusCode.STATUS_CODE_INVALID_PUBLICATION_ID,
               TSS.StatusCode.STATUS_CODE_SUBSCRIBED_ACCOUNTS_LIMIT_VIOLATION
               ],
    }

NEWORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING, 
               OS.Status.FILLED,
               OS.Status.SUSPENDED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]

    }

MODIFYORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.IN_MODIFY,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]
    }

CANCELORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.IN_CANCEL,
               OS.Status.CANCELLED,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.DISCONNECTED,
               OS.Status.EXPIRED],
    "Transit": [OS.Status.IN_TRANSIT,]
    }


ACTIVEATORDER_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [OS.Status.WORKING,
               OS.Status.ACTIVEAT,
               OS.Status.FILLED],
    "Reject": [OS.Status.REJECTED,
               OS.Status.APPROVE_REJECTED,
               OS.Status.EXPIRED,
               OS.Status.DISCONNECTED], 
    "Transit": [OS.Status.IN_TRANSIT,]
    }

GOFLAT_ORDERSTATUS_ENUMS_BOOL = {
    "Accept": [GFS.StatusCode.STATUS_CODE_COMPLETED],
    "Reject": [GFS.StatusCode.STATUS_CODE_TIMED_OUT,
               GFS.StatusCode.STATUS_CODE_FAILED]
    }

TRANSACTION_STATUS_ENUMS_BOOL = {}

# =============================================================================
# # Define Order statuses
# IN_TRANSIT = OrderStatus.Status.IN_TRANSIT  # Original order is sent to execution system.
# REJECTED = OrderStatus.Status.REJECTED # Order is rejected.
# WORKING = OrderStatus.Status.WORKING # Order is acknowledged by execution system and perhaps partially filled.
# EXPIRED = OrderStatus.Status.EXPIRED # Order is expired.
# IN_CANCEL = OrderStatus.Status.IN_CANCEL #Cancel request is sent to execution system.
# IN_MODIFY = OrderStatus.Status.IN_MODIFY # Modify request is sent to execution system.
# CANCELLED = OrderStatus.Status.CANCELLED # Order is canceled.
# FILLED = OrderStatus.Status.FILLED # Order is completely filled by execution system.
# SUSPENDED = OrderStatus.Status.SUSPENDED # Order is waiting submission to execution system.
# DISCONNECTED = OrderStatus.Status.DISCONNECTED # Order may be canceled because a disconnect occurred.
# ACTIVEAT = OrderStatus.Status.ACTIVEAT # Order will be placed at a specified time (waiting execution system to start accepting orders).
# APPROVE_REQUIRED = OrderStatus.Status.APPROVE_REQUIRED # Cross order is sent to exchange and waiting for approval from exchange and/or counter-parties.
# APPROVED_BY_EXCHANGE = OrderStatus.Status.APPROVED_BY_EXCHANGE
# APPROVE_REJECTED = OrderStatus.Status.APPROVE_REJECTED
# MATCHED = OrderStatus.Status.MATCHED
# PARTIALLY_MATCHED = OrderStatus.Status.PARTIALLY_MATCHED
# TRADE_BROKEN = OrderStatus.Status.TRADE_BROKEN
# =============================================================================
