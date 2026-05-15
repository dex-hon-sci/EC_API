#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 11:21:19 2025

@author: dexter
"""

from enum import Enum


# --- Status Enum ---
class OpStrategyStatus(Enum):
    LIVE = "Live"
    IDLE = "Idle"


class OpSignalStatus(Enum):
    INACTIVE = "Inactive"  # OpSignal
    ACTIVE = "Active"
    FREEZE = "Freeze"  # Only temporarily inactive.
    TERMINAL = "Terminated"  # when action tree is exhausted
    EXPIRED = "Expired"  # Terminated by time


class ActionStatus(Enum):
    PENDING = "Pending"
    SENT = "Sent"  # Payloads have been sent to the database
    COMPLETED = "Completed"  # Afrer receving a confirmation from the server
    CANCELLED = "Cancelled"


# --- Lifecycle ---
OPSTRATEGY_STATUS_LIFECYCLE: dict[OpStrategyStatus, list[OpStrategyStatus]] = {
    OpStrategyStatus.LIVE: [OpStrategyStatus.LIVE, OpStrategyStatus.IDLE],
    OpStrategyStatus.IDLE: [OpStrategyStatus.LIVE, OpStrategyStatus.IDLE],
}

OPSIGNAL_STATUS_LIFECYCLE: dict[OpSignalStatus, list[OpSignalStatus]] = {  # Work on this later
    OpSignalStatus.INACTIVE: [],
    OpSignalStatus.ACTIVE: [],
    OpSignalStatus.FREEZE: [],
    OpSignalStatus.TERMINAL: [],
    OpSignalStatus.EXPIRED: [],
}

ACTION_STATUS_LIFECYCLE: dict[ActionStatus, list[ActionStatus]] = {
    ActionStatus.PENDING: [ActionStatus.PENDING, ActionStatus.SENT, ActionStatus.CANCELLED],
    ActionStatus.SENT: [ActionStatus.SENT, ActionStatus.COMPLETED, ActionStatus.CANCELLED],
    ActionStatus.COMPLETED: [],
    ActionStatus.CANCELLED: [],
}
