#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 21:55:11 2025

@author: dexter
"""

import asyncio
import threading
import queue
from typing import Optional

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.ext.WebAPI import webapi_client

class CQGTransport:
    
    """
    Wraps the blocking CQG WebApiClient with:
      - one IO thread doing send/recv
      - a thread-safe outbound queue
      - an asyncio inbound queue
    Only incharge of sending messages. Recv msg is controlled by the router
    """

    def __init__(self, host_name: str, loop: asyncio.AbstractEventLoop):
        self._loop = loop
        self._client = webapi_client.WebApiClient()
        self._host_name = host_name

        # thread-safe outbound queue (ClientMsg to send)
        self._out_q: queue.Queue[ClientMsg] = queue.Queue()
        # async inbound queue (ServerMsg received)
        self.in_q: asyncio.Queue[ServerMsg] = asyncio.Queue()

        self._stop_evt = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        """Connect underlying CQG client (blocking, called once)."""
        self._client.connect(self._host_name)

    def start(self) -> None:
        """Start IO thread (must call connect() before this)."""

        def _io_loop():
            while not self._stop_evt.is_set():
                # 1) Send all pending outbound messages (if any)
                try:
                    while True:
                        msg = self._out_q.get_nowait()
                        self._client.send_client_message(msg)
                except queue.Empty:
                    pass

                # 2) Blocking receive from CQG
                server_msg = self._client.receive_server_message()
                # push into async queue in the event loop
                asyncio.run_coroutine_threadsafe(
                    self.in_q.put(server_msg),
                    self._loop,
                )

        self._thread = threading.Thread(target=_io_loop, daemon=True)
        self._thread.start()

    async def send(self, client_msg: ClientMsg) -> None:
        """Async-friendly send: enqueue a message for the IO thread."""
        def _put():
            self._out_q.put(client_msg)

        # run _put in a threadpool so we don't block the event loop
        await asyncio.get_running_loop().run_in_executor(None, _put)

    def stop(self) -> None:
        """Stop IO thread and close CQG connection."""
        self._stop_evt.set()
        if self._thread:
            self._thread.join(timeout=1.0)
        self._client.disconnect()

    @property
    def raw_client(self) -> webapi_client.WebApiClient:
        """Expose underlying client if you absolutely need it (try not to)."""
        return self._client    