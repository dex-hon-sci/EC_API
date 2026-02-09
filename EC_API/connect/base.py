#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:23:04 2025

@author: dexter
"""
# Native Python imports
import asyncio
from typing import Protocol
from EC_API.transport.base import Transport
from EC_API.transport.router import MessageRouter
from EC_API.connect.enums import ConnectionState

class Connect(Protocol):
    # Base class for websocket-like connection
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str):
        """
        Instantiation can immediately create connection to the server.
        One set of user_name + password for one Connect Object.
        """
        self._host_name = host_name
        self._user_name = user_name
        self._password = password       
        
        # State Control
        self.state = ConnectionState.UNKNOWN
        
        # Transport layer for async adaptation
        self._loop = asyncio.get_running_loop()
        self._transport = Transport()
        self._router = MessageRouter()

    # ---- Getter methods for class attributes ----
    @property
    def client(self):
        """
        Getter method for client connection object.
        """
        return self._client
    
    # ---- Life Cycle ----
    def start(self):
        """
        Set up and start connection via the Transport layer's method.
        Usually setting up router loop as well
        """
        ...
    
    async def stop(self):
        """
        Stop connection via the Transport layer's method.
        """
        ...
        
    # ---- Vendor specific functions templates ----
    async def connect(self):
        """
        Create connection to the server.
        State: UKNOWN -> CONNECTING/
        if it is successful, State: CONNECTING -> CONNECTED
        if it is not, State: CONNECTING -> DISCONNECTED
        """
        pass
        
    async def disconnect(self):
        """
        User initiated Disconnection sequence.
        State: CONNECTED/CONNECTED_LOGON/CONNECTED_LOGOFF -> DISCONNECTING
        if it is successful, State: DISCONNECTING -> DISCONNECTED
        if it is not, State: DISCONNECTING -> CONNECTED/CONNECTED_LOGON/CONNECTED_LOGOFF

        """
        ...

    async def logon(self):
        """
        User initiated Logon sequence. 
        if it is successful, State: CONNECTED -> CONNECTED_LOGON
        if it is not, State: CONNECTED -> CONNECTED

        """
        ...
    
    async def logoff(self):
        """
        User initiated Logoff sequence.
        if it is successful, State: CONNECTED_LOGON -> CONNECTED_LOGOFF
        if it is not, State: CONNECTED_LOGON -> CONNECTED_LOGON

        """
        ...
    
    def restore_request(self):
        """
        A Necessary restore connection method. Usually it take in a 
        session_token as an input to restore connection.
        State: DISCONNECTED -> RECONNECTING
        if it is successful, State: RECONNECTING -> CONNECTED
        if it is not, State: RECONNECTING -> DISCONNECTED

        """
        ...
    
    async def ping(self):
        """
        Used for Connection health check. Expect a Pong response message from
        server and calculate the time between send and recieve.
        If the wait time is above some threshold, the state can change
        from State: CONNECTECTED -> DISCONNECTED
        
        restore_request can then be called to attempt restoring connections.
        """
        ...

