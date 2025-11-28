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
        
        self.total_recv_cycle: int = 20
        self.total_send_cycle: int = 2
        self.recv_cycle_delay: int = 0
        self.send_cycle_delay: int = 0
        
    def connection(self):
        return self._connection
    


