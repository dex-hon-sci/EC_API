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
    status_check = False # For checking status_code existence
    succes_status_check = False # For checking succe state in status_code
    reject_status_check = False # For checking reject state in status_code
    trade_snapshot_check = False
    result_check = False # Check for result msg existence
    
    
class ValidMsgCheck(Protocol):
    # Interface for Valid msg checking in case we switch to a different
    # Market data service provider
    def __init__(self):
        self.para = MsgCheckPara()
    
    def status_check():
        pass
    
    def success_status_check():
        pass
    
    def reject_status_check():
        pass
    
    def result_check():
        pass
    
    
