#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
import asyncio
from typing import Any  # Hashable, Optional
import logging

logger = logging.getLogger(__name__)

# (msg_family, msg_type, id_field_name, id)
RouterKey = tuple[str, str, str, int | str]


class MessageRouter:
    def __init__(self):
        self._pending: dict[RouterKey, asyncio.Future] = {}

    def register_key(self, key: RouterKey) -> asyncio.Future:
        fut = asyncio.get_running_loop().create_future()

        if key in self._pending.keys():
            logger.error(
                "[Message Router] Router register key failed: key '{key}' already exist.",
                extra={"router_key": key}
            )
        self._pending[key] = fut

        # clearup code in case of user cancel
        def _cleanup(_):
            self._pending.pop(key, None)
        
        fut.add_done_callback(_cleanup)
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
        max_sub_size: int = 5,
        max_num_sym: int = 50,
        drop_if_full: bool = False
        ):
        # we assume one Stream Router per vendor
        self._subs: dict[int, list[asyncio.Queue]] = {}
        self._max_queue_size = max_queue_size
        self._max_subs_size = max_sub_size
        self._max_num_sym = max_num_sym
        self._drop_if_full = drop_if_full

    def subscribe(
        self,
        contract_id: int
        ) -> asyncio.Queue[Any] | None:
        # Add a new Queue to the list in case there is a new subscriber who
        # calls subscribe
        if len(self._subs) >= self._max_num_sym:
            logger.error("[Stream Router] Maximum number of contract subscribed exceeded.")
            return 
            
        if self._subs.get(contract_id):
            if len(self._subs[contract_id]) >= self._max_subs_size:
                logger.error(f"[Stream Router] Maximum subscribers has reached for this contract: {contract_id}")
                return

        q = asyncio.Queue(
            maxsize=self._max_queue_size) if self._max_queue_size else asyncio.Queue()

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
            
        if q not in lst:
            logger.error(f"[Stream Router] Unsubscribe failed. Input queue is not in the list of contract id:{contract_id}",
                         extra = {"contract_id": contract_id}
                         )
            return 
        
        if not lst and contract_id in self._subs:
            # Maybe do some backup for unconsumed data first here
            # Only delete when the streaming is completely done
            del self._subs[contract_id]

    async def publish(self, contract_id: int, item: Any) -> None:
        queues = self._subs.get(contract_id)
        if not queues:
            return
        
        # Put the latest data into the Async Queue inside the StreamRouter
        for q in self._subs.get(contract_id, []):
            #if self._drop_if_full:
            #    # Drop oldest 
            try:
                q.put_nowait(item)
            except asyncio.QueueFull:
                if self._drop_if_full:
                # safest fallback: drop anyway rather than deadlock
                    try:
                        q._queue.popleft()
                        q.put_nowait(item)
                    except Exception:
                        continue

                    
