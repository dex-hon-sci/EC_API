#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 03:11:13 2026

@author: dexter
"""
import time
from typing import Optional, Any, Callable
import aiosqlite
from EC_API.recorder.base import SQLSchemaTable, Recorder

def _from_dict_to_row(msg: dict[str, Any], schema: SQLSchemaTable) -> tuple[Any,...]:
    # This assume the schema colums name are exactly the same 
    # as the field names in a parsed message.
    return tuple([msg[col_name] for col_name, _ in schema.columns])

class SQLiteRecorder(Recorder):
    def __init__(
            self, 
            schema: SQLSchemaTable,
            db_address: str, 
            batch_size: int = 100, 
            flush_interval: float=5.0,
            to_row: Optional[Callable[[Any], tuple[Any]]] = None
        ):
        # DB setup
        self._schema: SQLSchemaTable = schema
        self._db_address: str = db_address
        self._db: Optional[aiosqlite.Connection] = None

        # Recorder Config
        self._batch_size: int= batch_size
        self._flush_interval: int = flush_interval #seconds
        
        # message format for logging
        # Conversion from raw message to DB format
        self._to_row: Callable[[Any], tuple[Any]] = to_row if to_row is not None else _from_dict_to_row
        
        # SQL commands
        self._insert_query: str = self._schema.insert_query('sqlite3')
        
        # Containers
        self._buf: list[tuple[Any],...] = list()

    @property
    def schema(self):
        return self._schema
    
    async def start(self) -> None:
        self._db = await aiosqlite.connect(self._db_address)
        await self._db.execute("PRAGMA journal_mode=WAL") # WAL
        await self._db.execute("PRAGMA synchronous=NORMAL") 
        await self._db.execute(self._schema.create_query())
        await self._db.commit()
        self._last_flush = time.monotonic()

    async def stop(self) -> None:
        await self._flush()
        await self._db.close()
    
    async def record(self, msg: Any) -> None:
        self._buf.append(self._to_row(msg, self._schema))
        
        if (len(self._buf)>=self._batch_size or 
            time.monotonic() - self._last_flush >= self._flush_interval
            ):
            await self._flush()
        
    async def _flush(self) -> None:
        await self._db.executemany(self._insert_query, self._buf)
        await self._db.commit()
        self._buf.clear()
        
        self._last_flush = time.monotonic()
    