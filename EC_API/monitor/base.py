#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:32:53 2025

@author: dexter
"""
from typing import Protocol
# Import EC_API scripts
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg
from EC_API.connect.base import Connect

class Monitor(Protocol):
    # An Object incharge of 
    def __init__(self, connection: Connect):
        self._connection = connection
        self._msg_id = 200 # just a starting number for message id
        
    def connection(self):
        return self._connection
    
    @property
    def msg_id(self):
        # msg_id updates every time it is called. 
        # This ID is shared by the entire Monitor object.
        self._msg_id += 1
        return self._msg_id 


