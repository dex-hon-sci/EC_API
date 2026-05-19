#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 23:54:33 2026

@author: dexter
"""
from EC_API.channel.base import Channel


class PipeChannel(Channel):
    def __init__(self):        
        ...
    def connect(self): ...
    def disconnect(self): ...
    async def broadcast(self): ...
    async def listen(self): ...