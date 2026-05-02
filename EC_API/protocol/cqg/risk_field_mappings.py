#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:17:36 2026

@author: dexter
"""

CQG_RISK_FIELD_MAP: dict[str, str] = {
    "qty_max":        "qty",
    "qty_min":        "qty",
    "price_max":      "limit_price",
    "price_min":      "limit_price",
    "stop_price_max": "stop_price",
    "stop_price_min": "stop_price",
}