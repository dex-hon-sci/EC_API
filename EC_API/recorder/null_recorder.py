#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 02:57:04 2026

@author: dexter
"""

class NullRecorder:
    def __init__(self):...
    
    def start(self) -> None: ...
    
    def stop(self) -> None: ...
    
    async def record(self, msg) -> None:...