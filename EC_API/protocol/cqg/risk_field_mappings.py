#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 01:17:36 2026

@author: dexter
"""

CQG_RISK_FIELD_MAP: dict[str, str] = {
    "qty_max":        "qty_significant",
    "price_max":      "scaled_limit_price",
    "price_min":      "scaled_limit_price",
    "stop_price_max": "scaled_stop_price",
    "stop_price_min": "scaled_stop_price",
}