#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:21:19 2025

@author: dexter
"""
from enums import Enum

class OpSignalStatus(Enum):
    INACTIVE = "Inactive" # OpSignal 
    ACTIVE = "Active" 
    FREEZE = "Freeze" # Only temporarily inactive.
    TERMINAL = "Terminated" # when action tree is exhausted
    EXPIRED = "Expired" # Terminated by time

    
class ActionStatus(Enum):
    PENDING = "Pending"
    FILLED = "Filled"
    VOID = "Cancelled"

