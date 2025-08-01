#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 09:34:29 2025

@author: dexter
"""
from dataclasses import dataclass
from typing import Protocol
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

@dataclass
class MsgCheckPara:
    recv_status = False # For checking status_code existence
    recv_succes_status = False # For checking succe state in status_code
    recv_reject_status = False # For checking reject state in status_code
    recv_trade_snapshot = False
    recv_result = False # Check for result msg existence
    
    
class ValidMsgCheck(Protocol):
    # Interface for Valid msg checking in case we switch to a different
    # Market data service provider
    
    def status_check(self):
        pass
    
    def success_status_check(self):
        pass
    
    def reject_status_check(self):
        pass
    
    def result_check(self):
        # Existence check for the correct message
        pass
    
    
