#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 21:55:11 2025

@author: dexter
"""

from typing import Protocol, Any

class Transport(Protocol):
    """
    Provider-agnostic transport interface.

    It represents a bidirectional connection to some broker API
    (WebSocket, TCP, etc.), abstracting away whether it is backed
    by a blocking client, threads, asyncio, etc.

    Concrete implementations (CQG, IB, Binance, ...) should:
      - manage their own connection lifecycle
      - expose async send/recv for higher layers
    """
    # ----
    def start(self) -> None:
        """
        Start any background IO machinery (threads, tasks, etc.).

        For a blocking client wrapped in a thread (e.g. CQG WebApiClient),
        this would typically:
          - connect the underlying client if needed
          - spin up the reader loop thread
        """
        ...

    def stop(self) -> None:
        """
        Stop background IO and close the underlying connection.
        Should be idempotent and safe to call on shutdown.
        """
        ...
        
    # ----
    def _send_loop(self): ...

    def _recv_loop(self): ...

    # ----
    async def send(self, msg: Any) -> None:
        """
        Asynchronously enqueue or send an outbound message.

        The type of `msg` is provider-specific:
          - CQG: a ClientMsg protobuf
          - IB: some wrapper / request type
          - Binance: JSON/dict/etc.

        This must not block the event loop.
        """
        ...

    async def recv(self) -> Any:
        """
        Asynchronously receive the next inbound message.

        This should:
          - suspend until a message is available
          - return the raw provider message type (e.g. ServerMsg for CQG)

        Higher layers (protocol parsers, routers) will interpret it.
        """
        ...