#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 03:11:13 2026

@author: dexter
"""
import aiosqlite 

class SQLiteRecorder:
    def __init__(self):
        self._schema = None
        self._insert_query: str = None
        
    def start(self) -> None: ...
    
    def stop(self) -> None: ...
    
    async def record(self, msg) -> None:...