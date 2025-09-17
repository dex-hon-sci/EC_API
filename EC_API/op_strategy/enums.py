#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:21:19 2025

@author: dexter
"""
from enums import Enum

class OpSignalStatus(Enum):
    ACTIVE = "Active"
    FREEZE = "Freeze" # Only temporarily inactive.
    INACTIVE = "Inactive" # OpSignal Shutdown
    
class ActionStatus(Enum):
    FILLED = "Filled"
    PENDING = "Pending"
    VOID = "Cancelled"

