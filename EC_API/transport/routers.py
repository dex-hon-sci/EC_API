#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
import asyncio
from typing import Any  # Hashable, Optional
#import logging
from EC_API.exceptions import (
    DuplicateRouterKeyError,
    UnknownSubscriptionError, SubscriptionQueueMismatchError,
    MaxSymbolsExceededError, MaxSubscribersExceededError
    )

#logger = logging.getLogger(__name__)

# (msg_family, msg_type, id_field_name, id)
RouterKey = tuple[str, str, str, int | str]


class MessageRouter:
    def __init__(self):
        self._pending: dict[RouterKey, asyncio.Future] = {}

    def register_key(self, key: RouterKey) -> asyncio.Future:
        fut = asyncio.get_running_loop().create_future()

        if key in self._pending.keys():
            raise DuplicateRouterKeyError(f"Router register key failed: key '{key}' already exist.")
            #logger.error(
            #    "[Message Router] Router register key failed: key '{key}' already exist.",
            #    extra={"router_key": key}
            #)
        
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
        drop_if_full: bool = True,
        drop_policy: str = "drop_oldest"
        ):
        # we assume one Stream Router per vendor
        self._subs: dict[int, list[asyncio.Queue]] = {}
        self._max_queue_size = max_queue_size
        self._max_subs_size = max_sub_size
        self._max_num_sym = max_num_sym
        self._drop_if_full = drop_if_full
        self.drop_policy = drop_policy

    def subscribe(
        self,
        contract_id: int
        ) -> asyncio.Queue[Any] | None:
        # Add a new Queue to the list in case there is a new subscriber who
        # calls subscribe
        if len(self._subs) >= self._max_num_sym:
            raise MaxSymbolsExceededError("Maximum number of contract subscribed exceeded.")
            #logger.error(
            #    "[Stream Router] Maximum number of contract subscribed exceeded."
            #    )
            #return 
            
        if self._subs.get(contract_id):
            if len(self._subs[contract_id]) >= self._max_subs_size:
                #logger.error(
                #    f"[Stream Router] Maximum subscribers has reached for this contract: {contract_id}."
                #    )
                raise MaxSubscribersExceededError(f"Maximum subscribers has reached for this contract: {contract_id}.")

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
        if not lst:
            #logger.error(
            #    "[Stream Router] Retrival of {contract_id} failed. Contract ID: {contract_id} is not ini the router.",
            #    extra = {"contract_id": contract_id}
            #    )
            raise UnknownSubscriptionError(f"Retrival of {contract_id} failed. Contract ID: {contract_id} is not ini the router.")
            
        if q not in lst:
            #logger.error(f"[Stream Router] Unsubscribe failed. Input queue is not in the list of contract id:{contract_id}",
            #             extra = {"contract_id": contract_id})
            raise SubscriptionQueueMismatchError(f"Unsubscribe failed. Input queue is not in the list of contract id:{contract_id}.") 

        lst.remove(q)

        if not lst and contract_id in self._subs:
            # Maybe do some backup for unconsumed data first here
            # Only delete when the streaming is completely done
            del self._subs[contract_id]

    async def publish(
            self,
            contract_id: int, 
            item: Any,
            cool_time = 0.1
        ) -> None:
        queues = self._subs.get(contract_id)
        if not queues:
            return
        
        for q in list(queues):
            if not self._drop_if_full:
                await q.put(item)
                continue
            
            try:
                q.put_nowait(item)
            except asyncio.QueueFull:
                if self._drop_if_full:
                    if self.drop_policy == "drop_oldest":
                        try:
                            q._queue.popleft()
                            q.put_nowait(item)
                        except Exception:
                            continue
                    elif self.drop_policy == "drop_latest":
                        continue
                    else:
                        continue
            await asyncio.sleep(cool_time)
                    
