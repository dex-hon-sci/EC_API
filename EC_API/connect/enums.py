#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 10:04:11 2025

@author: dexter
"""

from enum import Enum

class ConnectionState(Enum):
    # Account Login related enums
    CONNECTED_DEFAULT = "Connected-Default" # Connection is Established without either logon or logoff
    CONNECTED_LOGON = "Connected-Logon" # Connection is Established and Logon is success
    CONNECTED_LOGOFF = "Connected-Logoff" # Connection is Established and Lofoff is success
    # Connection related enums
    CONNECTING = "Connecting" # Attempting to Establish communication (handshake not confirm)
    DISCONNECTED = "Disconnected" # Connection is lost (Ping indicate problem)
    RECONNECTING = "Reconnecting" # Reconnection based on Fault tolerance policy
    CLOSING = "Closing" # User initiated Disconnection (Disconnect command)
    CLOSED = "Closed" # State once the underlying connection is closed.    
    #Aborted = "Aborted"
    UNKNOWN = "Unknown" # Default Setting, to be changed once connection is established
    

# --- State Lifecycle ---
CONNECT_STATES_LIFECYCLE = {
    ConnectionState.UNKNOWN: [
        ConnectionState.CONNECTING
        ],
    ConnectionState.CONNECTING: [
        ConnectionState.RECONNECTING,
        ConnectionState.CONNECTED_DEFAULT,
        ConnectionState.DISCONNECTED
        ],
    ConnectionState.CONNECTED_DEFAULT: [
        ConnectionState.CONNECTED_LOGON,
        ConnectionState.RECONNECTING,
        ConnectionState.DISCONNECTED
        ],
    ConnectionState.RECONNECTING: [
        ConnectionState.CONNECTED_DEFAULT,
        ConnectionState.DISCONNECTED
        ],
    ConnectionState.CONNECTED_LOGON: [
        ConnectionState.CONNECTED_LOGOFF,
        ConnectionState.DISCONNECTED
        ],
    ConnectionState.CONNECTED_LOGOFF: [
        ConnectionState.CONNECTED_LOGON,
        ConnectionState.DISCONNECTED,
        #ConnectionState.CLOSING
        ],
    ConnectionState.DISCONNECTED: [
        ConnectionState.RECONNECTING,
        ConnectionState.CLOSING
        ],
    ConnectionState.CLOSING: [
        ConnectionState.CLOSED
        ],
    ConnectionState.CLOSED: [] # End State
    }
