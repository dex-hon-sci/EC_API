#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
import asyncio
from typing import Any #Hashable, Optional

Key = tuple[str, int]  # (server_msg_type, request_id)

class MessageRouter:
    def __init__(self):
        self._pending: dict[Key, asyncio.Future] = {}

    def register_key(self, key: Key) -> asyncio.Future:
        fut = asyncio.get_running_loop().create_future()
        # show error if key already exists ...
        self._pending[key] = fut
        return fut
    
    def register_predicate():
        pass

    def on_message(self, key: Key, msg: Any) -> bool:
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
        
# =============================================================================
# from __future__ import annotations
# import asyncio
# from typing import Dict, Tuple, Any
# 
# from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
# from EC_API.msg_validation.cqg.mapping import MAP_RESPONSES_TYPES_STR
# from EC_API.msg_validation.cqg.mapping import MAP_STATUS_ENUMS  # optional
# 
# 
# MsgKey = Tuple[str, int]  # (msg_type, request_id)
# 
# 
# class MessageRouter:
#     """
#     Futures-based request/response matcher.
# 
#     - register(key) -> Future
#     - on_message(msg) -> resolves the right Future when a matching reply arrives
#     """
# 
#     def __init__(self) -> None:
#         self._pending: dict[MsgKey, asyncio.Future] = {}
# 
#     def register(self, key: MsgKey) -> asyncio.Future:
#         loop = asyncio.get_running_loop()
#         fut = loop.create_future()
#         self._pending[key] = fut
#         return fut
# 
#     def on_message(self, server_msg: ServerMsg) -> None:
#         msg_type = server_msg.WhichOneof("message")
# 
#         # For e.g. information_reports, order_statuses, etc.,
#         # we assume the message carries a request_id field.
#         req_id = extract_request_id(server_msg, msg_type)
#         key = (msg_type, req_id)
# 
#         fut = self._pending.pop(key, None)
#         if fut and not fut.done():
#             fut.set_result(server_msg)
# 
# =============================================================================
