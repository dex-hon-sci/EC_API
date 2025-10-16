#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:21:19 2025

@author: dexter
"""
from enum import Enum

class OpSignalStatus(Enum):
    INACTIVE = "Inactive" # OpSignal 
    ACTIVE = "Active" 
    FREEZE = "Freeze" # Only temporarily inactive.
    TERMINAL = "Terminated" # when action tree is exhausted
    EXPIRED = "Expired" # Terminated by time

    
class ActionStatus(Enum):
    PENDING = "Pending"
    SENT = "Sent" # Payloads have been sent to the database
    COMPLETED = "Completed"
    VOID = "Cancelled"

