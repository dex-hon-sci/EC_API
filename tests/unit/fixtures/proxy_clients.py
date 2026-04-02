#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:23:10 2025

@author: dexter
"""
# Python imports
import queue
import asyncio
# EC_API imports
#from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API._typing import ServerMsgType, ClientMsgType

class FakeCQGClient:
    # For the dependecy injection in unit tests
    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.sent_messages: list[ClientMsgType] = []
        self._incoming = queue.Queue()
        
    def connect(self, host_name: str):
        self.connected = True

    def disconnect(self):
        self.disconnected = True
        # Optionally unblock receive by putting a sentinel
        self._incoming.put(None)

    def send_client_message(self, msg: ClientMsgType):
        self.sent_messages.append(msg)

    def receive_server_message(self) -> ServerMsgType:
        """
        Blocking read. For tests, we simulate this with queue.get().
        """
        msg = self._incoming.get()
        if msg is None:
            # Treat sentinel as "no more messages"
            raise RuntimeError("Client closed.")
        return msg

    def push_incoming(self, msg: ServerMsgType):
        """Helper: push a message so transport.recv() can eventually see it."""
        self._incoming.put(msg)
        
class FakeTransport:
    def __init__(self):
        self.in_q: asyncio.Queue[ServerMsgType] = asyncio.Queue()
        self.out_q: queue.Queue[ClientMsgType] = queue.Queue()

    async def recv(self) -> ServerMsgType:
        return await self.in_q.get()
    
    async def send(self, msg: ClientMsgType) -> None:
        self.out_q.put(msg)
        
    def connect(self):...
    def start(self):...
    def stop(self):...