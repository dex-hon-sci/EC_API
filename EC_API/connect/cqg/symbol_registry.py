#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:23:04 2026

@author: dexter
"""
import logging
from EC_API.utility.symbol_registry import SymbolRegistry
from EC_API.connect.cqg.base import ConnectCQG

logger = logging.getLogger(__name__)

class SymbolRegistryCQG(SymbolRegistry):
    def __init__(self, conn: ConnectCQG):
        super().__init__()
        self.conn = conn
        
    # --- CQG function call --
    async def resolve_symbol(
            self,
            symbol_name: str
            ) -> bool:...
