#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 19:27:33 2025

@author: dexter
"""

from enum import Enum

class PayloadStatus(Enum):
    PENDING = "Pending" # Starting, in Storage or in Chamber
    READY = "Ready" # Ready to be sent, necessary condition before being sent
    LOCKED = "Locked" # Lock Payload during processing
    SENT = "Sent" # Transition state, move from Chamber to ShellPile
    ACK = "Acknowledged" # Ack by server
    FILLED = "Filled" # Confirm Filled, change state in ShellPile
    VOID = "Failed" # Confirm Cancelled, change state in ShellPile
    ARCHIVED = "Archived" # Order was not sent and reach its time limit, move from Chamber to Archieve
    