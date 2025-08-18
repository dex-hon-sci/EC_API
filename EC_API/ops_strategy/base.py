#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 12:52:55 2025

@author: dexter

Operational Strategy module
"""
from typing import Protocol
from enums import Enum

class OpsSignalStatus(Enum):
    pass

class OpsSignal(Protocol):
    """
    OpsSignal contain the cool-down mechanism.
    """
    pass

class OpsStrategy(Protocol):
    """
    Base class of Operational Strategy
    
    Input: Monitor info, specify data type, sizes and x.
    DB_address: somewhere to save the outputs
    Output: Signal/Payload. 
    """
    def __init__(self):
        pass
    
    def make_payloads(self):
        pass