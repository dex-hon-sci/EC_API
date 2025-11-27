#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 17:28:27 2025

@author: dexter
"""
import asyncio
import threading 
from typing import Optional
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.ext.WebAPI import webapi_client

class CQGTransport:
    # Transport layer between user and websocket
    # enable async tasks using the same websocket
    
    def __init__(self, client: webapi_client, loop:asyncio.AbstractEventLoop):
        self._client = client
        self._loop = loop
        
        self.inqueue = asyncio.Queue[ClientMsg] = asyncio.Queue()
        self.outqueue = asyncio.Queue[ServerMsg] = asyncio.Queue()
        
        self._stop_evt = threading.Event()
        self._thread: Optional[threading.Thread] = None
        
    def start()->None:
        pass
    
    async def send()->None:
        pass
    
    def stop()->None:
        pass
        