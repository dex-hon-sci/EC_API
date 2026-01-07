#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 07:46:28 2026

@author: dexter
"""

import asyncio
from dataclasses import dataclass
from typing import Dict, Tuple, Optional, Any

@dataclass(frozen=True)
class SubHandle:
    key: Tuple[str, int]   # e.g. ("orders", account_id) or ("trades", contract_id)
    token: int             # unique token per acquisition (optional)

class SubscriptionManager:
    def __init__(self, *, transport: Any, router: Any, conn: Any):
        self._transport = transport
        self._router = router
        self._conn = conn

        self._lock = asyncio.Lock()
        self._refcounts: Dict[Tuple[str, int], int] = {}
        self._active: Dict[Tuple[str, int], bool] = {}
        self._token_ctr = 0

    async def ensure_orders_subscribed(self, *, account_id: int, timeout: float = 2.0) -> SubHandle:
        key = ("orders", account_id)

        async with self._lock:
            n = self._refcounts.get(key, 0)
            self._refcounts[key] = n + 1
            if n > 0:
                # Already subscribed or in-progress; we treat it as active.
                self._token_ctr += 1
                return SubHandle(key=key, token=self._token_ctr)

            # First user: we will perform the actual subscribe.
            self._active[key] = False
            self._token_ctr += 1
            handle = SubHandle(key=key, token=self._token_ctr)

        # Do the actual subscribe outside the lock
        rid = self._conn.msg_id()
        client_msg = build_trade_subscription_msg(
            trade_subscription_id=rid,  # or proper sub id field
            subscribe=True,
            skip_orders_snapshot=False,
            # include account scope if CQG requires it
        )
        fut = self._router.register(("trade_subscription_statuses", rid))
        try:
            await self._transport.send(client_msg)
            await asyncio.wait_for(fut, timeout=timeout)
        except Exception:
            # Roll back refcount on failure
            async with self._lock:
                self._refcounts[key] = max(self._refcounts.get(key, 1) - 1, 0)
                if self._refcounts[key] == 0:
                    self._refcounts.pop(key, None)
                    self._active.pop(key, None)
            raise
        finally:
            self._router.unregister(("trade_subscription_statuses", rid))

        async with self._lock:
            self._active[key] = True
        return handle

    async def release(self, handle: SubHandle, *, timeout: float = 2.0) -> None:
        key = handle.key

        async with self._lock:
            n = self._refcounts.get(key, 0)
            if n <= 0:
                return  # or raise; depends on how strict you want to be
            n -= 1
            if n > 0:
                self._refcounts[key] = n
                return

            # n == 0 => last user is releasing; unsubscribe
            self._refcounts.pop(key, None)
            was_active = self._active.pop(key, False)

        if not was_active:
            return

        rid = self._conn.msg_id()
        client_msg = build_trade_subscription_msg(
            trade_subscription_id=rid,
            subscribe=False,
            skip_orders_snapshot=True,
        )
        fut = self._router.register(("trade_subscription_statuses", rid))
        try:
            await self._transport.send(client_msg)
            await asyncio.wait_for(fut, timeout=timeout)
        finally:
            self._router.unregister(("trade_subscription_statuses", rid))
