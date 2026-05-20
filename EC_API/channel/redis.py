#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 00:29:07 2026

@author: dexter
"""
import tomllib
from typing import Optional
import msgpack
import redis.asyncio as aioredis
from EC_API.channel.base import Channel
from EC_API.utility.error_handlers import toml_loader_error_handler
from EC_API.exceptions import (
    ChannelMissingSettingError,
    ChannelBroadcastError,
    ChannelListenError,
    ConfigInputError,
    ConfigFormatError
    )

class RedisChannel(Channel):
    def __init__(self):        
        # --- global settings
        self.r: aioredis.Redis = None
        self.pipeline = None
        self._pubsub = None
        
        self.host_name: str = None
        
        # --- Redis Stream settings
        self.out_streams: Optional[list[str]] = None
        self.in_streams: Optional[list[str]] = None
        
        self.maxlen_out_stream: int = 50_000
        # for redis stream message tracking
        self.last_ids: Optional[dict[str, str]] = None
        
        # We only allow one active listener to stream at a time
        self._active_listeners: set[str] = set()
        
    def load(self, path: str):
        # add a load error handler here
        with toml_loader_error_handler(ConfigInputError, ConfigFormatError):
            with open(path, mode="rb") as f:
                para = tomllib.load(f)
        
                self.host_name = para.get("host_name", {})
                if not self.host_name:
                    raise KeyError("Field 'host_name' is missing in the toml file.")
                
                if not para.get("streams"):
                    raise KeyError("Field: 'streams' is missing in the toml file.")
                    
                self.in_streams = para["streams"].get("in_streams", [])
                self.out_streams = para["streams"].get("out_streams", [])
                
                if not (self.in_streams or self.out_streams):
                    raise KeyError("In field 'streams', at least one of these must be present: 'in_streams' and 'out_streams'.")
                
                self.last_ids = {name: '$' for name in self.in_streams}

    def connect(self):
        if not self.host_name:
            raise ChannelMissingSettingError("Missing URL to start a redis server.")
            
        self.r = aioredis.Redis.from_url(self.host_name['URL'], decode_responses=False)
        self._pubsub = self.r.pubsub()
        self.pipeline = self.r.pipeline()

    async def disconnect(self):
        if not self.r:
            raise ChannelMissingSettingError("Redis server was not initiated.")
        await self._pubsub.close()
        await self.r.aclose()
    
    # --- Regular method. Redis default to stream
    async def broadcast(self, parsed_msg: tuple, stream_name:str, data_name: str='data') -> None:
        try:
           await self.r.xadd(stream_name, {data_name: msgpack.packb(parsed_msg)},
                             maxlen=self.maxlen_out_stream, approximate=True)
        except Exception as e:
            raise ChannelBroadcastError(str(e))

    async def listen(self, stream_name: str, data_name: str='data') -> tuple | None:
        if stream_name in self._active_listeners:
            raise RuntimeError(f"{stream_name} already has an active listener")
        self._active_listeners.add(stream_name)

        try:
            # [stream_name, [(id, fields_dict),...]]
            l = await self.r.xread(count=1, block=0, streams = {stream_name: self.last_ids[stream_name]})
            if not l:
                return None
            
            self.last_ids[stream_name]: str = l[0][1][-1][0]
            return msgpack.unpackb(l[0][1][-1][1][data_name])
        except Exception as e:
            raise ChannelListenError(str(e))
        
        finally:
            self._active_listeners.discard(stream_name)

    # --- Special method. For heartbeat or transient messages
    async def subscribe_pubsub(self, channel: str) -> None:
        await self._pubsub.subscribe(channel)

    async def unsubscribe_pubsub(self, channel: str) -> None:
        await self._pubsub.unsubscribe(channel)
    
    async def broadcast_pubsub(self, parsed_msg: tuple, stream_name: str, data_name: str='data') -> None:
        try:
            await self.r.publish(stream_name, msgpack.packb(parsed_msg))
        except Exception as e:
            raise ChannelBroadcastError(str(e))
    
    async def listen_pubsub(self):
        try:
          async for message in self._pubsub.listen():
              if message['type'] == 'message':
                  return msgpack.unpackb(message['data'])
        except Exception as e:
            raise ChannelListenError(str(e))
