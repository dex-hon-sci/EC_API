#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  2 14:36:45 2025

@author: dexter
"""
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import OrderStatus
# Map Server reponse order status to Payload status
ORDS2PAYLOAD_STATUS_MAP = {
    OrderStatus.IN_TRANSIT: PayloadStatus.ACK,
    OrderStatus.REJECTED: PayloadStatus.VOID,
    OrderStatus.WORKING:  PayloadStatus.SENT,
    OrderStatus.EXPIRED: PayloadStatus.SENT, 
    OrderStatus.IN_CANCEL: PayloadStatus.ACK, 
    OrderStatus.IN_MODIFY: PayloadStatus.ACK, 
    OrderStatus.CANCELLED: PayloadStatus.FILLED,
    OrderStatus.FILLED: PayloadStatus.FILLED,
    OrderStatus.SUSPENDED: PayloadStatus.FILLED,
    OrderStatus.DISCONNECTED: PayloadStatus.VOID,
    OrderStatus.ACTIVEAT: PayloadStatus.FILLED,
    OrderStatus.APPROVE_REQUIRED: PayloadStatus.ACK,
    OrderStatus.APPROVED_BY_EXCHANGE: PayloadStatus.ACK,
    OrderStatus.APPROVE_REJECTED: PayloadStatus.VOID, 
    OrderStatus.MATCHED: PayloadStatus.FILLED,
    OrderStatus.PARTIALLY_MATCHED: PayloadStatus.FILLED,
    OrderStatus.TRADE_BROKEN: PayloadStatus.VOID
    }