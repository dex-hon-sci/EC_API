#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 02:57:04 2026

@author: dexter
"""
from EC_API.recorders.base import Recorder


class NullRecorder(Recorder):
    def __init__(self):...
    async def start(self) -> None: pass
    async def stop(self) -> None: pass
    async def record(self, msg) -> None: pass