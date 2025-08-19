#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:23:04 2025

@author: dexter
"""
# Native Python imports
from typing import Protocol

class Connect(Protocol):
    # Base class for websocket-like connection
    def __init__(self, 
                 host_name: str, 
                 user_name: str, 
                 password: str):
        self._host_name = host_name
        self._user_name = user_name
        self._password = password
        
        # Immediate connection
    
    @property
    def client(self):
        # return client connection object
        return self._client

    def logon(self):
        pass
    
    def logoff(self):
        pass
    
    def disconnect(self):
        pass
