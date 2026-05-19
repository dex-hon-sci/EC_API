#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:29:07 2026

@author: dexter
"""
import tomllib
import asyncio
from typing import Optional
import msgpack
import redis.asyncio as aioredis
from EC_API.channel.base import Channel

#REDIS_URL = "redis://localhost:6379"
class RedisChannel(Channel):
    def __init__(self):        
        self.r: aioredis.Redis = None
        self.pipe = None
        
        self.host: str = None
        self.out_stream: str = None
        self.in_stream: str = None
        
        self.last_id = '$'
        
    def load(self, path: str):
        with open(path, mode="rb") as f:
            para = tomllib.load(f)
            self.host = para.get("host", "")
            self.out_stream = para.get("out_stream", "")
            self.in_stream = para.get("in_stream", "")
    
    async def connect(self, url: str):
        self.r = aioredis.Redis.from_url(self.host, decode_responses=False)
        self.pipe = self.r.pipeline()

    async def disconnect(self):
        self.r.close()
    
    async def broadcast(self, parsed_msg: tuple, data_name: str='data') -> None:
       await self.r.xadd(self.out_stream, {data_name: msgpack.packb(parsed_msg)},
                          maxlen=50_000, approximate=True)
    
    async def listen(self, stream_name: str, data_name: str='data') -> tuple:
        # [stream_name, [(id, fields_dict),...]]
        l = await self.r.xread(count=1, streams = {stream_name: self.last_id})
        self.last_id: str = l[0][1][-1][0]
        return msgpack.unpackb(l[0][1][-1][1][data_name])
        
