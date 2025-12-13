#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 18:23:10 2025

@author: dexter
"""
# Python imports
import queue
# EC_API imports
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

class FakeCQGClient:
    # For the dependecy injection in unit tests
    def __init__(self):
        self.connected = False
        self.disconnected = False
        self.sent_messages: list[ClientMsg] = []
        self._incoming = queue.Queue()
        
    def connect(self, host_name: str):
        self.connected = True

    def disconnect(self):
        self.disconnected = True
        # Optionally unblock receive by putting a sentinel
        self._incoming.put(None)

    def send_client_message(self, msg: ClientMsg):
        self.sent_messages.append(msg)

    def receive_server_message(self) -> ServerMsg:
        """
        Blocking read. For tests, we simulate this with queue.get().
        """
        msg = self._incoming.get()
        if msg is None:
            # Treat sentinel as "no more messages"
            raise RuntimeError("Client closed")
        return msg

    def push_incoming(self, msg: ServerMsg):
        """Helper: push a message so transport.recv() can eventually see it."""
        self._incoming.put(msg)