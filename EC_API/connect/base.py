#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:23:04 2025

@author: dexter
"""
# Native Python imports
from typing import Protocol
from EC_API.connect.enums import ConnectionState

class Connect(Protocol):
    # Base class for websocket-like connection
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str):
        """
        Instantiation can immediately create connection to the server.

        """
        self._host_name = host_name
        self._user_name = user_name
        self._password = password       
        self.state = ConnectionState.UNKNOWN
    
    @property
    def client(self):
        """
        Getter method for client connection object.
        """
        return self._client
    
    def connect(self):
        """
        Create connection to the server.
        State: UKNOWN -> CONNECTING/
        if it is successful, State: CONNECTING -> CONNECTED
        if it is not, State: CONNECTING -> DISCONNECTED
        """
        pass

    def logon(self):
        """
        User initiated Logon sequence. 
        if it is successful, State: CONNECTED -> CONNECTED_LOGON
        if it is not, State: CONNECTED -> CONNECTED

        """
        pass
    
    def logoff(self):
        """
        User initiated Logoff sequence.
        if it is successful, State: CONNECTED_LOGON -> CONNECTED_LOGOFF
        if it is not, State: CONNECTED_LOGON -> CONNECTED_LOGON

        """
        pass
    
    def restore_request(self):
        """
        A Necessary restore connection method. Usually it take in a 
        session_token as an input to restore connection.
        State: DISCONNECTED -> RECONNECTING
        if it is successful, State: RECONNECTING -> CONNECTED
        if it is not, State: RECONNECTING -> DISCONNECTED

        """
        pass
    
    def disconnect(self):
        """
        User initiated Disconnection sequence.
        State: CONNECTED/CONNECTED_LOGON/CONNECTED_LOGOFF -> DISCONNECTING
        if it is successful, State: DISCONNECTING -> DISCONNECTED
        if it is not, State: DISCONNECTING -> CONNECTED/CONNECTED_LOGON/CONNECTED_LOGOFF

        """
        pass
