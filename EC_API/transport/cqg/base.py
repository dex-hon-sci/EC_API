#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 21:55:11 2025

@author: dexter
"""
import logging
import asyncio
import threading
import queue
from typing import Optional

from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.ext.WebAPI import webapi_client

logger = logging.getLogger(__name__)

class TransportCQG:
    """
    Wraps the blocking CQG WebApiClient with:
      - Two IO thread doing send/recv
      - a thread-safe outbound queue
      - an asyncio inbound queue
    Only incharge of sending messages. Recv msg is controlled by the router
    """

    def __init__(
            self, 
            host_name: str, 
            loop: asyncio.AbstractEventLoop,
            client: Optional[webapi_client.WebApiClient] = None #
            ):
        self._loop = loop
        self._client = webapi_client.WebApiClient() if client is None else client
        self._host_name = host_name

        # thread-safe outbound queue (ClientMsg to send)
        self._out_q: queue.Queue[ClientMsg] = queue.Queue()
        # async inbound queue (ServerMsg received)
        self._in_q: asyncio.Queue[ServerMsg] = asyncio.Queue()

        self._stop_evt = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def connect(self) -> None:
        self._client.connect(self._host_name)

    # --- writer and reader loops -------------
    def _send_loop(self) -> None:
        # writer loop for send
        while not self._stop_evt.is_set():
            msg = self._out_q.get()
            if msg is None:
                break  # sentinel for shutdown
            try:
                self._client.send_client_message(msg)
            except Exception:
                # log, maybe set a flag, etc.
                break
            
    def _recv_loop(self) -> None:
        # reader loop for recv
        while not self._stop_evt.is_set():
            try:
                server_msg = self._client.receive_server_message()
            except Exception:
                # log, break on fatal error
                break

            if server_msg is None:
                # sentinel or EOF
                break

            asyncio.run_coroutine_threadsafe(
                self._in_q.put(server_msg),
                self._loop,
            ) 
    
    # --- Thread based msg ---------
    def start(self) -> None:
        self._send_thread = threading.Thread(
            target=self._send_loop, daemon=True,
            name = "TransportCQG-send_loop"
        )
        self._recv_thread = threading.Thread(
            target=self._recv_loop, daemon=True,
            name = "TransportCQG-recv_loop"
        )
        
        self._send_thread.start()
        self._recv_thread.start()
        
    def stop(self) -> None:
        """Stop IO thread and close CQG connection."""        
        self._stop_evt.set()
        # wake send loop
        self._out_q.put(None)
        # close client to poke receive
        try:
            self._client.disconnect()
        except Exception:
            pass
        
        if self._send_thread:
            self._send_thread.join(timeout=1.0)
        if self._recv_thread:
            self._recv_thread.join(timeout=1.0)
    # --------------------
    
    # --- Public API -----
    async def send(self, client_msg: ClientMsg) -> None:
        """Async-friendly send: enqueue a message for the IO thread."""
        self._out_q.put(client_msg)
        
    async def recv(self) -> ServerMsg:
        return await self._in_q.get()
    # -------------------
    