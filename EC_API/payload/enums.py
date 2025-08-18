#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:27:33 2025

@author: dexter
"""

from enum import Enum

class PayloadStatus(Enum):
    PENDING = "Pending" # Starting, in Storage or in Chamber
    SENT = "Sent" # Transition state, move from Chamber to ShellPile
    FILLED = "Filled" # Confirm Filled, change state in ShellPile
    VOID = "Cancelled" # Confirm Cancelled, change state in ShellPile
    ARCHIVED = "Archived" # Order was not sent and reach its time limit, move from Chamber to Archieve
    