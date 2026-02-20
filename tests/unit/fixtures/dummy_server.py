#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 06:34:47 2026

@author: dexter
"""
import socket


class DummyWSServer:
    
    def __init__(
            self,
            host: str,
            port: int,
        ):
        self._host = host
        self._port = port
        
    @property
    def host(self) -> str:
        return self._host
    
    @property
    def port(self) -> int:
        return self._port
    
    @property
    def url(self) -> str:
        return f"https://{self.host}:{self.port}"
    
    async def start(self):
        return 
    
    async def stop(self):
        return 
    # Build up message
    # Unleash
    
    
import pytest

@pytest.fixture
async def dummy_server():
    server = DummyWSServer("", 0)
    
def decoder():...
async def place_standard_reponses():...
    
