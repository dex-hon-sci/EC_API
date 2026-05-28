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
from EC_API._typing import ServerMsgType, ClientMsgType
from EC_API.exceptions import (
    TransportConnectError, 
    TransportDisconnectError
    )

class FakeCQGClient:
    # For the dependecy injection in unit tests
    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.sent_messages: list[ClientMsgType] = []
        self._incoming = queue.Queue()
        self._closed: bool = False
        
    def connect(self, host_name: str):
        self.connected = True

    def disconnect(self):
        self.disconnected = True
        # Optionally unblock receive by putting a sentinel
        self._incoming.put(None)
        self._closed = True
        
    def send_client_message(self, msg: ClientMsgType):
        self.sent_messages.append(msg)

    def receive_server_message(self) -> ServerMsgType:
        """
        Blocking read. For tests, we simulate this with queue.get().
        """
        msg = self._incoming.get()
        if msg is None or self._closed:
            # Treat sentinel as "no more messages"
            return None
        return msg

    def push_incoming(self, msg: ServerMsgType):
        """Helper: push a message so transport.recv() can eventually see it."""
        self._incoming.put(msg)
        
class FakeTransport:
    def __init__(self):
        self.in_q: asyncio.Queue[ServerMsgType] = asyncio.Queue()
        self.out_q: queue.Queue[ClientMsgType] = queue.Queue()

        self.fail_connect: bool = False
        self.fail_disconnect: bool = False
        self.fail_start: bool = False
        self.fail_stop: bool = False
        
    async def recv(self) -> ServerMsgType:
        return await self.in_q.get()
    
    async def send(self, msg: ClientMsgType) -> None:
        self.out_q.put(msg)
        
    def connect(self) -> bool:
        if self.fail_connect:
            raise TransportConnectError("Fail to Connect")
        return True
    
    def disconnect(self) -> bool:
        if self.fail_disconnect:
            raise TransportDisconnectError("Fail to Disconnect")
        return True
    
    def start(self) -> bool:
        if self.fail_start:
            return False
        return True
    
    def stop(self) -> bool:
        if self.fail_stop:
            raise TransportDisconnectError("Fail to Stop")
        return True