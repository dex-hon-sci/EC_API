#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
import asyncio
from typing import Any #Hashable, Optional

RouterKey = tuple[str, int]  # (server_msg_type, request_id)

class MessageRouter:
    def __init__(self):
        self._pending: dict[RouterKey, asyncio.Future] = {}

    def register_key(self, key: RouterKey) -> asyncio.Future:
        fut = asyncio.get_running_loop().create_future()
        # show error if key already exists ...
        if key in self._pending.keys():
            print(f'key already exist:{key}')
        self._pending[key] = fut
        return fut

    def on_message(self, key: RouterKey, msg: Any) -> bool:
        fut = self._pending.pop(key, None)
        if fut is None:
            return False
        if not fut.done():
            fut.set_result(msg)
        return True

    def fail_all(self, exc: BaseException) -> None:
        for k, fut in list(self._pending.items()):
            if not fut.done():
                fut.set_exception(exc)
        self._pending.clear()
        
        
class StreamRouter:
    def __init__(
            self, 
            max_queue_size: int = 1_000, 
            drop_if_full: bool = False
        ):
        # we assume one Stream Router per vendor
        self._subs: dict[int, list[asyncio.Queue]] = {}
        self._max_queue_size = max_queue_size
        self._drop_if_full = drop_if_full

    def subscribe(
            self, 
            contract_id: int
        ) -> asyncio.Queue[Any]:
        q = asyncio.Queue(maxsize=self._max_queue_size) if self._max_queue_size else asyncio.Queue()
        # Add a new Queue to the list in case there is a new subscriber who
        # calls subscribe
        self._subs.setdefault(contract_id, []).append(q)
        return q
    
    def unsubscribe(
            self, 
            contract_id: int, 
            q: asyncio.Queue
        ) -> None:
        
        lst = self._subs.get(contract_id, [])
        if q in lst:
            lst.remove(q)
        if not lst and contract_id in self._subs:
            # Maybe do some backup for unconsumed data first here
            # Only delete when the streaming is completely done
            
            del self._subs[contract_id]
            
    async def publish(self, contract_id: int, item: Any) -> None:
        # Put the latest data into the Async Queue inside the StreamRouter
        for q in self._subs.get(contract_id, []):
            if self._drop_if_full:
                # Drop newest (or implement drop-oldest policy)
                continue
            try:
                await q.put_nowait(item)
            except asyncio.QueueFull:
                
                if not self._drop_if_full:
                    # safest fallback: drop anyway rather than deadlock
                    pass

        

