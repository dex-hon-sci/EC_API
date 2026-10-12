#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 20:57:06 2026

@author: dexter
"""
from typing import Protocol, Any

class ServerBrain(Protocol):
    def __init__(self):...
    async def response_logic(self, msg: Any, **kwargs):...