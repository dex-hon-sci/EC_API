#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:29:07 2026

@author: dexter
"""
from typing import Optional
import msgpack
import redis.asyncio as aioredis
from EC_API.channel.base import Channel

#REDIS_URL = "redis://localhost:6379"
#redis = aioredis.Redis.from_url(REDIS_URL, decode_responses=True)

class RedisChannel(Channel):
    def __init__(self, host: str):
        self.host: str = host
        self.r: aioredis.Redis = None
        self.pipe = None
    
    async def connect(self, url: str):
        self.r = aioredis.Redis.from_url(self.host, decode_responses=True)
        self.pipe = self.r.pipe

    async def disconnect(self):
        self.r.close()
    
    async def broadcast(self):...
    
    async def listen(self):...