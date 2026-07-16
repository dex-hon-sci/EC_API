#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 03:25:06 2026

@author: dexter
"""
from typing import Protocol

class Recorder(Protocol):
    def __init__(self):...
    
    async def record(self):...