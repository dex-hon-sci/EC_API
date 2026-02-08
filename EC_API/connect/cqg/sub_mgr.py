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
    
    
class SubscriptionManagerCQG:
    def __init__():
        pass
    
    async def ensure_trade_subscription():
        # A function that ensure trade subscriptions is present 
        pass

    async def ensure_market_data():
        pass
    
    async def release_market_data():
        pass


from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager

class SubscriptionManagerCQG:
    def __init__(self, transport, router, builders, parsers, request_id_gen):
        self._transport = transport
        self._router = router
        self._b = builders
        self._p = parsers
        self._next_id = request_id_gen

        self._lock = asyncio.Lock()

        self._trade_subscribed = False
        self._trade_inflight: asyncio.Future[None] | None = None

        self._symbol_cache: dict[str, int] = {}
        self._md_refcount: dict[int, int] = {}
        self._md_inflight: dict[int, asyncio.Future[None]] = {}

    # ---------- TRADE SUBSCRIPTION ----------
    async def ensure_trade_subscription(self, *, timeout: float = 5.0) -> None:
        async with self._lock:
            if self._trade_subscribed:
                return
            if self._trade_inflight is not None:
                fut = self._trade_inflight
            else:
                fut = asyncio.get_running_loop().create_future()
                self._trade_inflight = fut

                rid = self._next_id()
                msg = self._b.build_trade_subscribe(request_id=rid)  # you’ll implement builder
                key = ("ordering", "trade_subscription_status", rid)
                reply_fut = self._router.register(key)

                # Send outside lock to avoid holding lock across IO
                async def _do():
                    try:
                        await self._transport.send(msg)
                        server_msg = await asyncio.wait_for(reply_fut, timeout=timeout)
                        ok = self._p.parse_trade_sub_status(server_msg)
                        if not ok:
                            raise RuntimeError("Trade subscription failed")
                        async with self._lock:
                            self._trade_subscribed = True
                        fut.set_result(None)
                    except Exception as e:
                        fut.set_exception(e)
                    finally:
                        async with self._lock:
                            self._trade_inflight = None

                asyncio.create_task(_do())

        # Await outside lock
        await asyncio.wait_for(fut, timeout=timeout)

    # ---------- SYMBOL RESOLVE ----------
    async def resolve_symbol(self, symbol: str, *, timeout: float = 5.0) -> int:
        async with self._lock:
            if symbol in self._symbol_cache:
                return self._symbol_cache[symbol]

        rid = self._next_id()
        msg = self._b.build_resolve_symbol(symbol=symbol, request_id=rid)
        key = ("monitor", "resolve_symbol_result", rid)
        fut = self._router.register(key)
        await self._transport.send(msg)

        server_msg = await asyncio.wait_for(fut, timeout=timeout)
        contract_id = self._p.parse_resolve_symbol(server_msg)

        async with self._lock:
            self._symbol_cache[symbol] = contract_id

        return contract_id

    # ---------- MARKET DATA SUBSCRIPTION ----------
    async def ensure_market_data(self, symbol: str, *, timeout: float = 5.0) -> int:
        contract_id = await self.resolve_symbol(symbol, timeout=timeout)

        async with self._lock:
            # already subscribed?
            if contract_id in self._md_refcount:
                self._md_refcount[contract_id] += 1
                return contract_id

            # in-flight subscribe?
            if contract_id in self._md_inflight:
                inflight = self._md_inflight[contract_id]
                self._md_refcount[contract_id] = 1  # “claim” usage
            else:
                inflight = asyncio.get_running_loop().create_future()
                self._md_inflight[contract_id] = inflight
                self._md_refcount[contract_id] = 1

                rid = self._next_id()
                msg = self._b.build_md_subscribe(contract_id=contract_id, request_id=rid)
                key = ("monitor", "md_subscription_status", rid)
                reply_fut = self._router.register(key)

                async def _do():
                    try:
                        await self._transport.send(msg)
                        server_msg = await asyncio.wait_for(reply_fut, timeout=timeout)
                        ok = self._p.parse_md_sub_status(server_msg)
                        if not ok:
                            raise RuntimeError(f"MD subscription failed for {contract_id}")
                        inflight.set_result(None)
                    except Exception as e:
                        inflight.set_exception(e)
                        # rollback refcount on failure
                        async with self._lock:
                            self._md_refcount.pop(contract_id, None)
                    finally:
                        async with self._lock:
                            self._md_inflight.pop(contract_id, None)

                asyncio.create_task(_do())

        # wait for subscription to be confirmed
        await asyncio.wait_for(inflight, timeout=timeout)
        return contract_id

    async def release_market_data(self, contract_id: int, *, timeout: float = 5.0) -> None:
        async with self._lock:
            if contract_id not in self._md_refcount:
                return
            self._md_refcount[contract_id] -= 1
            if self._md_refcount[contract_id] > 0:
                return
            # drop to 0: unsubscribe
            self._md_refcount.pop(contract_id, None)

        rid = self._next_id()
        msg = self._b.build_md_unsubscribe(contract_id=contract_id, request_id=rid)
        key = ("monitor", "md_unsubscribe_status", rid)
        fut = self._router.register(key)
        await self._transport.send(msg)
        server_msg = await asyncio.wait_for(fut, timeout=timeout)
        ok = self._p.parse_md_unsub_status(server_msg)
        if not ok:
            # don’t re-add refcount automatically; log + alert
            raise RuntimeError(f"MD unsubscribe failed for {contract_id}")

    @asynccontextmanager
    async def market_data(self, symbol: str):
        cid = await self.ensure_market_data(symbol)
        try:
            yield cid
        finally:
            await self.release_market_data(cid)


# =============================================================================
#     
# 
# class SubscriptionManager:
#     def __init__(self, *, transport: Any, router: Any, conn: Any):
#         self._transport = transport
#         self._router = router
#         self._conn = conn
# 
#         self._lock = asyncio.Lock()
#         self._refcounts: Dict[Tuple[str, int], int] = {}
#         self._active: Dict[Tuple[str, int], bool] = {}
#         self._token_ctr = 0
# 
#     async def ensure_orders_subscribed(self, *, account_id: int, timeout: float = 2.0) -> SubHandle:
#         key = ("orders", account_id)
# 
#         async with self._lock:
#             n = self._refcounts.get(key, 0)
#             self._refcounts[key] = n + 1
#             if n > 0:
#                 # Already subscribed or in-progress; we treat it as active.
#                 self._token_ctr += 1
#                 return SubHandle(key=key, token=self._token_ctr)
# 
#             # First user: we will perform the actual subscribe.
#             self._active[key] = False
#             self._token_ctr += 1
#             handle = SubHandle(key=key, token=self._token_ctr)
# 
#         # Do the actual subscribe outside the lock
#         rid = self._conn.msg_id()
#         client_msg = build_trade_subscription_msg(
#             trade_subscription_id=rid,  # or proper sub id field
#             subscribe=True,
#             skip_orders_snapshot=False,
#             # include account scope if CQG requires it
#         )
#         fut = self._router.register(("trade_subscription_statuses", rid))
#         try:
#             await self._transport.send(client_msg)
#             await asyncio.wait_for(fut, timeout=timeout)
#         except Exception:
#             # Roll back refcount on failure
#             async with self._lock:
#                 self._refcounts[key] = max(self._refcounts.get(key, 1) - 1, 0)
#                 if self._refcounts[key] == 0:
#                     self._refcounts.pop(key, None)
#                     self._active.pop(key, None)
#             raise
#         finally:
#             self._router.unregister(("trade_subscription_statuses", rid))
# 
#         async with self._lock:
#             self._active[key] = True
#         return handle
# 
#     async def release(self, handle: SubHandle, *, timeout: float = 2.0) -> None:
#         key = handle.key
# 
#         async with self._lock:
#             n = self._refcounts.get(key, 0)
#             if n <= 0:
#                 return  # or raise; depends on how strict you want to be
#             n -= 1
#             if n > 0:
#                 self._refcounts[key] = n
#                 return
# 
#             # n == 0 => last user is releasing; unsubscribe
#             self._refcounts.pop(key, None)
#             was_active = self._active.pop(key, False)
# 
#         if not was_active:
#             return
# 
#         rid = self._conn.msg_id()
#         client_msg = build_trade_subscription_msg(
#             trade_subscription_id=rid,
#             subscribe=False,
#             skip_orders_snapshot=True,
#         )
#         fut = self._router.register(("trade_subscription_statuses", rid))
#         try:
#             await self._transport.send(client_msg)
#             await asyncio.wait_for(fut, timeout=timeout)
#         finally:
#             self._router.unregister(("trade_subscription_statuses", rid))
# =============================================================================
