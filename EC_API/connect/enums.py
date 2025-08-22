#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 10:04:11 2025

@author: dexter
"""

from enum import Enum

class ConnectionState(Enum):
    CONNECTED = "Connected" # Handshake is completed
    CONNECTING = "Connecting" # Attempting to Establish communication
    DISCONNECTED = "Disconnected" # Connection is lost
    RECONNECTING = "Reconnecting" # Reconnection based on Fault tolerance policy
    CLOSING = "Closing" # User initiated Disconnection
    CLOSED = "Closed" # State once the underlying connection is closed.    
    UNKNOWN = "Unknown" # Default Setting, to be changed once connection is established
    
