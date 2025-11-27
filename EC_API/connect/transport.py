#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 17:45:18 2025

@author: dexter
"""
import asyncio
import threading
from typing import Optional

class Transport:
    # Transport layer between user and websocket
    # enable async tasks using the same websocket
    
    def __init__(self, 
                 #client: webapi_client, 
                 loop:asyncio.AbstractEventLoop):
        self._client = None
        self._loop = loop
        
        self.inqueue = asyncio.Queue = asyncio.Queue()
        self.outqueue = asyncio.Queue = asyncio.Queue()
        
        self._stop_evt = threading.Event()
        self._thread: Optional[threading.Thread] = None
        
    def start()->None:
        pass
    
    async def send()->None:
        pass
    
    def stop()->None:
        pass
        