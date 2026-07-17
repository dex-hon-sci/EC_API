#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 03:11:13 2026

@author: dexter
"""
import time
import aiosqlite
from EC_API.recorder.base import SQLSchemaTable

class SQLiteRecorder:
    def __init__(self, db_address: str, batch_size: int = 100):
        self._schema: SQLSchemaTable = None
        self._db_address: str = db_address
        
        self._batch_size: int= batch_size
        self._insert_query: str = self._schema.insert_query('sqlite3')
        
        self._buf: list[str] = list()

    async def start(self) -> None:
        self.db = await aiosqlite.connect(self._db_address)

    async def stop(self) -> None:
        await self._flush()
        await self.db.close()
    
    async def record(self, msg) -> None:
        self._buf.append(msg)
        
        if len(self._buf)>=self._batch_size:
            await self._flush()
        
    def _flush(self) -> None:
        await self.db.executemany(self._insert_query, self._buf)
        await self.db.commit()
        self._buf.clear()
        
        self._last_flush = time.monotonic()
        
        
        
# =============================================================================
# 
# class SQLiteRecorder:
#     def __init__(self, schema, path, batch_size=1000, flush_interval=1.0):
#         self._schema = schema
#         self._path = path
#         self._insert = schema.insert_query()
#         self._batch_size = batch_size
#         self._flush_interval = flush_interval
#         self._buf: list[tuple] = []
#         self._last_flush = 0.0
#         self._db: aiosqlite.Connection | None = None
# 
#     async def start(self) -> None:
#         self._db = await aiosqlite.connect(self._path)
#         await self._db.execute("PRAGMA journal_mode=WAL")      # concurrent reads, faster writes
#         await self._db.execu")     # safe under WAL, farfewer fsyncs than FULL
#         await self._db.execu))
#         await self._db.commit()
#         self._last_flush = t
# 
#     async def record(self, r
#         self._buf.append(row)
#         if (len(self._buf) >
#                 or time.monotonic() - self._last_flush >= self._flush_interval):
#             await self._flus
# 
#     async def _flush(self) -
#         if not self._buf:
#             return
#         await self._db.executemany(self._insert, self._buf)
#         await self._db.commi
#         self._buf.clear()
#         self._last_flush = t
# 
#     async def stop(self) ->
#         await self._flush()          # never lose the tail
#         await self._db.close
# =============================================================================
