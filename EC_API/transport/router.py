#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 16:40:57 2025

@author: dexter
"""
from __future__ import annotations
import asyncio
from typing import Dict, Tuple, Any

from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg
from EC_API.msg_validation.cqg.mapping import MAP_RESPONSES_TYPES_STR
from EC_API.msg_validation.cqg.mapping import MAP_STATUS_ENUMS  # optional


MsgKey = Tuple[str, int]  # (msg_type, request_id)


class MessageRouter:
    """
    Futures-based request/response matcher.

    - register(key) -> Future
    - on_message(msg) -> resolves the right Future when a matching reply arrives
    """

    def __init__(self) -> None:
        self._pending: dict[MsgKey, asyncio.Future] = {}

    def register(self, key: MsgKey) -> asyncio.Future:
        loop = asyncio.get_running_loop()
        fut = loop.create_future()
        self._pending[key] = fut
        return fut

    def on_message(self, server_msg: ServerMsg) -> None:
        msg_type = server_msg.WhichOneof("message")

        # For e.g. information_reports, order_statuses, etc.,
        # we assume the message carries a request_id field.
        req_id = extract_request_id(server_msg, msg_type)
        key = (msg_type, req_id)

        fut = self._pending.pop(key, None)
        if fut and not fut.done():
            fut.set_result(server_msg)


def extract_request_id(msg: ServerMsg, msg_type: str) -> int:
    """
    Extract request_id from a server message, depending on its type.
    You already have some mapping logic in msg_validation.cqg.mapping;
    this function centralizes that.
    """
    # Example for information_reports and market_data_subscription_statuses.
    # Adapt to your actual proto structure:
    if msg_type == "information_reports":
        return msg.information_reports[0].request_id
    elif msg_type == "market_data_subscription_statuses":
        return msg.market_data_subscription_statuses.request_id
    elif msg_type == "order_statuses":
        return msg.order_statuses.request_id
    # ... add other cases as needed ...

    raise ValueError(f"Don't know how to extract request_id for msg_type={msg_type}")
