#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
import asyncio
import logging
from typing import Any  # Hashable, Optional
from EC_API._typing import RouterKey
from EC_API.exceptions import (
    DuplicateRouterKeyError,
    UnknownSubscriptionError, SubscriptionQueueMismatchError,
    MaxSymbolsExceededError, MaxSubscribersExceededError,
    InvalidDroppingPolicy
    )

logger = logging.getLogger(__name__)

class MessageRouter:
    def __init__(self):
        self.pending: dict[RouterKey, asyncio.Future] = {}
        
    @property
    def pending_count(self) -> int:
        return len(self.pending)

    def register_key(self, key: RouterKey) -> asyncio.Future:
        fut = asyncio.get_running_loop().create_future()

        if key in self.pending.keys():
            msg = f"Router register key failed: key '{key}' already exist."
            logger.error("[%s] %s", __class__.__name__, msg)
            raise DuplicateRouterKeyError(msg)

        self.pending[key] = fut

        # clearup code in case of user cancel
        def _cleanup(_):
            self.pending.pop(key, None)
        
        fut.add_done_callback(_cleanup)
        return fut

    def on_message(self, key: RouterKey, msg: Any) -> bool:
        fut = self.pending.pop(key, None)
        if fut is None:
            return False
        if not fut.done():
            fut.set_result(msg)
        return True

    def fail_all(self, exc: BaseException) -> None:
        for k, fut in list(self.pending.items()):
            if not fut.done():
                fut.set_exception(exc)
        self.pending.clear()


class StreamRouter:
    def __init__(
        self,
        max_queue_size: int = 1_000, # max amount of data points
        max_sub_size: int = 5, # max number of subs per symbol
        max_num_sym: int = 50, # max number of symbols
        drop_if_full: bool = True,
        drop_policy: str = "drop_oldest"
        ):
        # we assume one Stream Router per vendor
        self._subs: dict[int|str, list[asyncio.Queue]] = {}
        self._max_queue_size = max_queue_size
        self._max_subs_size = max_sub_size
        self._max_num_sym = max_num_sym
        self._drop_if_full = drop_if_full
        
        if drop_policy not in {"drop_oldest", "drop_latest"}:
            raise InvalidDroppingPolicy("Invalid dropping policy. It must be either:'drp_oldest' or 'drop_latest'.")
        self.drop_policy = drop_policy
        
    @property
    def sub_id_count(self) -> int:
        return len(self._subs)
    
    def subscriber_count(self, sub_id: int | str) -> int:
        if not self._subs.get(sub_id):
            msg = f"Retrival of {sub_id} failed. Sub ID: {sub_id} is not in the router."
            logger.error("[%s] %s", __class__.__name__, msg)
            raise UnknownSubscriptionError(msg)
        return len(self._subs[sub_id])
    
    def subscribe(
        self,
        sub_id: int | str
        ) -> asyncio.Queue[Any] | None:
        # Add a new Queue to the list in case there is a new subscriber who
        # calls subscribe
        if len(self._subs) >= self._max_num_sym:
            msg = "Maximum number of contract subscribed exceeded."
            logger.error("[%s] %s", __class__.__name__, msg)
            raise MaxSymbolsExceededError(msg)
            
        if self._subs.get(sub_id):
            if len(self._subs[sub_id]) >= self._max_subs_size:
                msg = f"Maximum subscribers has reached for this contract: {sub_id}."
                logger.error("[%s] %s", __class__.__name__, msg)
                raise MaxSubscribersExceededError(msg)

        q = asyncio.Queue(
            maxsize=self._max_queue_size) if self._max_queue_size else asyncio.Queue()

        self._subs.setdefault(sub_id, []).append(q)
        return q

    def unsubscribe(
        self,
        sub_id: int|str,
        q: asyncio.Queue
        ) -> None:

        lst = self._subs.get(sub_id, [])
        if not lst:
            msg = f"Retrival of {sub_id} failed. Sub ID: {sub_id} is not in the router."
            logger.error("[%s] %s", __class__.__name__, msg)
            raise UnknownSubscriptionError(msg)
            
        if q not in lst:
            msg = f"Unsubscribe failed. Input queue is not in the list of id:{sub_id}."
            logger.error("[%s] %s", __class__.__name__, msg)
            raise SubscriptionQueueMismatchError(msg)

        lst.remove(q)

        if not lst and sub_id in self._subs: # delete subbed symbol when it is empty
            # Maybe do some backup for unconsumed data first here
            # Only delete when the streaming is completely done
            del self._subs[sub_id]

    async def publish(
            self,
            sub_id: int | str, 
            item: Any,
            cool_time = 0.001
        ) -> None:
        queues = self._subs.get(sub_id)
        if not queues:
            return
        
        for q in list(queues):
            if not self._drop_if_full:
                await q.put_nowait(item)
                continue
            
            try:
                q.put_nowait(item)
            except asyncio.QueueFull:
                if self._drop_if_full:
                    if self.drop_policy == "drop_oldest":
                        try:
                            q.get_nowait()
                            q.put_nowait(item)
                        except Exception:
                            msg = f"[{__class__.__name__}] Publish unsuccessful at queue full: {item}."
                            logger.warning(msg)
                            continue
                    elif self.drop_policy == "drop_latest":
                        try:
                            q._queue.pop()
                            q._queue.append(item)
                        except Exception:
                            msg =  f"[{__class__.__name__}] Publish unsuccessful at queue full: {item}."
                            logger.warning(msg)
                            continue

