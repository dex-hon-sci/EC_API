#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:23:04 2025

@author: dexter
"""
from typing import Protocol, Any
from EC_API.connect.enums import ConnectionState

class Connect(Protocol):

    # --- Properties ---
    @property
    def state(self) -> ConnectionState:
        ...

    @property
    def client(self): ...

    @property
    def transport(self): ...

    # --- Context manager ---
    async def __aenter__(self) -> "Connect": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool: ...

    # --- Lifecycle ---
    def rid(self) -> int: ...
    def start(self) -> bool:
        """
        Set up and start connection via the Transport layer's method.
        Usually setting up router loop as well
        """
        ...
    async def stop(self) -> bool:
        """
        Stop connection via the Transport layer's method.
        """
        ...

    # --- Session ---
    async def logon(self, **kwargs) -> dict[str, Any] | None: 
        """
        User initiated Logon sequence. 
        if it is successful, State: CONNECTED -> CONNECTED_LOGON
        if it is not, State: CONNECTED -> CONNECTED

        """
        ...
    async def logoff(self) -> dict[str, Any] | None:
        """
        User initiated Logoff sequence.
        if it is successful, State: CONNECTED_LOGON -> CONNECTED_LOGOFF
        if it is not, State: CONNECTED_LOGON -> CONNECTED_LOGON

        """
        ...
    async def restore_request(self, **kwargs) -> dict[str, Any] | None: 
        """
        A Necessary restore connection method. Usually it take in a 
        session_token as an input to restore connection.
        State: DISCONNECTED -> RECONNECTING
        if it is successful, State: RECONNECTING -> CONNECTED
        if it is not, State: RECONNECTING -> DISCONNECTED

        """
        ...

    # --- Heartbeat ---
    async def ping(self, token: str | None = None) -> dict[str, Any] | None: 
        """
        Used for Connection health check. Expect a Pong response message from
        server and calculate the time between send and recieve.
        If the wait time is above some threshold, the state can change
        from State: CONNECTECTED -> DISCONNECTED
        
        restore_request can then be called to attempt restoring connections.
        """
        ...
    async def pong(self, token: str, ping_utc_time: int, pong_utc_time: int) -> None: ...

    # --- Symbol ---
    async def resolve_symbol(self, symbol: str) -> dict[str, Any] | None: ...
    async def unsubscribe_symbol(self, symbol: str) -> None: ...
