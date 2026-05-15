#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:32:53 2025

@author: dexter
"""

from typing import Protocol, Any, AsyncIterator
from EC_API.connect.enums import ConnectionState
from EC_API.monitor.enums import MktDataSubLevel


class Monitor(Protocol):
    # --- Properties ---
    @property
    def conn(self): ...

    @property
    def state(self) -> ConnectionState: ...

    @property
    def timeout(self) -> float | int: ...

    # --- Context manager ---
    async def __aenter__(self) -> "Monitor": ...
    async def __aexit__(self, *args) -> bool: ...

    # --- Core ---
    def rid(self) -> int: ...
    def stream(self, symbol_name: str, level: MktDataSubLevel) -> AsyncIterator[Any]: ...
