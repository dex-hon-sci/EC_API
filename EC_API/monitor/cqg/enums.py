#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 00:23:11 2025

@author: dexter
"""
from enum import Enum, auto


class MktDataSubLevelCQG(Enum):
    LEVEL_SETTLEMENTS = auto()
    LEVEL_TRADES_BBA_DETAILED_DOM = auto()
    LEVEL_END_OF_DAY = auto()


