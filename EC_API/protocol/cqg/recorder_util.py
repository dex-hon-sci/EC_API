#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 23:57:10 2026

@author: dexter
"""
from typing import Any
from EC_API.recorders.base import SQLSchemaTable

# to_row functions flatten nested message and extract conddensed info, output a flat dict
def order_status_to_row_default(
        msg: dict[str, Any], schema: SQLSchemaTable
        ) -> dict[str, Any]:...
    

def position_status_to_row_default(
        msg: dict[str, Any], schema: SQLSchemaTable
        ) -> dict[str, Any]:...


def account_summary_to_row_default(
        msg: dict[str, Any], schema: SQLSchemaTable
        ) -> dict[str, Any]:...
