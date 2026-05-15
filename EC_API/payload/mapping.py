#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 14:36:45 2025

@author: dexter
"""

from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import OrderStatus
from EC_API.protocol.cqg.risk_field_mappings import CQG_RISK_FIELD_MAP

# Map Server reponse order status to Payload status
# Internal → Payload (in payload/mapping.py)
ORDS2PAYLOAD_STATUS_MAP = {
    OrderStatus.PENDING: PayloadStatus.ACK,
    OrderStatus.OPEN: PayloadStatus.SENT,
    OrderStatus.FILLED: PayloadStatus.FILLED,
    OrderStatus.PARTIAL: PayloadStatus.FILLED,
    OrderStatus.CANCELLED: PayloadStatus.VOID,
    OrderStatus.REJECTED: PayloadStatus.VOID,
    OrderStatus.EXPIRED: PayloadStatus.VOID,
    OrderStatus.ERROR: PayloadStatus.VOID,
}


PRETRADE_RISKCHECK_VENDORS_MAP = {"cqg": CQG_RISK_FIELD_MAP}

# =============================================================================
#     CQG_OrdStatus.Status.IN_TRANSIT: OrderStatus.PENDING,
#     CQG_OrdStatus.Status.REJECTED: OrderStatus.REJECTED,
#     CQG_OrdStatus.Status.WORKING: OrderStatus.OPEN,
#     CQG_OrdStatus.Status.EXPIRED: OrderStatus.EXPIRED,
#     CQG_OrdStatus.Status.IN_CANCEL: OrderStatus.PENDING,
#     CQG_OrdStatus.Status.IN_MODIFY: OrderStatus.PENDING,
#     CQG_OrdStatus.Status.CANCELLED: OrderStatus.CANCELLED,
#     CQG_OrdStatus.Status.FILLED: OrderStatus.FILLED,
#     CQG_OrdStatus.Status.SUSPENDED: OrderStatus.OPEN,
#     CQG_OrdStatus.Status.DISCONNECTED: OrderStatus.ERROR,
#     CQG_OrdStatus.Status.ACTIVEAT: OrderStatus.PENDING,
#     CQG_OrdStatus.Status.APPROVE_REQUIRED: OrderStatus.PENDING, #OrderStatus.APPROVE_REQUIRED,
#     CQG_OrdStatus.Status.APPROVED_BY_EXCHANGE: OrderStatus.OPEN, #OrderStatus.APPROVED_BY_EXCHANGE,
#     CQG_OrdStatus.Status.APPROVE_REJECTED: OrderStatus.REJECTED,
#     CQG_OrdStatus.Status.MATCHED: OrderStatus.FILLED,#OrderStatus.MATCHED,
#     CQG_OrdStatus.Status.PARTIALLY_MATCHED: OrderStatus.PARTIAL,#OrderStatus.PARTIALLY_MATCHED,
#     CQG_OrdStatus.Status.TRADE_BROKEN: OrderStatus.ERROR,
# =============================================================================
