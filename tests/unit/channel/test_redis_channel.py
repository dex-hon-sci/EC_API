#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:52:59 2026

@author: dexter
"""
import time
import asyncio
import subprocess
from pathlib import Path
import pytest
import msgpack
import redis.asyncio as aioredis
from EC_API.channel.redis import RedisChannel
from EC_API.exceptions import (
    ConfigInputError, 
    ConfigFormatError,
    ChannelMissingSettingError,
    ChannelBroadcastError,
    ChannelListenError
    )

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
TEST_TOML_TCP_SOCKET = FIXTURES_DIR / "test_redis_channel_setup_tcp_socket.toml"
TEST_TOML_UDS = FIXTURES_DIR / "test_redis_channel_setup_uds.toml"

# ---- Lifecycle ----
def test_redis_channel_load_tcp_valid() -> None:
    RC = RedisChannel()
    RC.load(TEST_TOML_TCP_SOCKET)
    assert RC.host_name['URL'] == "redis://localhost:16379"
    assert RC.in_streams == ["mkt_data:cqg", "mkt_data:fix"]
    assert RC.out_streams == ["processed_data"]
    assert list(RC.last_ids.keys()) == ["mkt_data:cqg", "mkt_data:fix"]
    assert list(RC.last_ids.values()) == ["0", "0"]
    
def test_redis_channel_load_uds_valid() -> None:
    RC = RedisChannel()
    RC.load(TEST_TOML_UDS)
    assert RC.host_name['URL'] == "unix:///tmp/redis.sock"
    assert RC.in_streams == ["mkt_data:cqg", "mkt_data:fix"]
    assert RC.out_streams == ["processed_data"]
    assert list(RC.last_ids.keys()) == ["mkt_data:cqg", "mkt_data:fix"]
    assert list(RC.last_ids.values()) == ["0", "0"]
    
BAD_CONFIGS = [
    # (toml_bytes, expected_exception)
    (b"this is not valid toml ===", ConfigInputError),
    (b'[streams]\nin_streams = ["s1"]', ConfigFormatError),  # no host_name
    (b'[host_name]\nURL = "redis://localhost:16379"', ConfigFormatError),  # no streams
    (b'[host_name]\nURL = "redis://localhost:16379"\n[streams]', ConfigFormatError),  # streams empty
    (b'[host_name]\nURL = "redis://localhost:16379"\n[streams]\nin_streams=[]\nout_streams=[]', ConfigFormatError) # at least one of the streams has to be present
]

@pytest.mark.parametrize("content, exc", BAD_CONFIGS)
def test_redis_channel_load_invalid_config(tmp_path, content, exc):
    f = tmp_path / "config.toml"
    f.write_bytes(content)
    with pytest.raises(exc):
        RedisChannel(path=str(f))

def test_redis_channel_load_invalid_missing_file():
    with pytest.raises(ConfigInputError):
        RedisChannel(path="/nonexistent/config.toml")
 
@pytest.mark.asyncio
async def test_redis_channel_connect_valid() -> None:
    RC = RedisChannel(TEST_TOML_TCP_SOCKET)
    await RC.connect()
    assert isinstance(RC.r, aioredis.Redis)
    assert isinstance(RC.pipeline, aioredis.client.Pipeline)
    assert isinstance(RC._pubsub, aioredis.client.PubSub)
    
@pytest.mark.asyncio   
async def test_redis_channel_connect_invalid_hostname_empty() -> None:
    RC = RedisChannel()
    with pytest.raises(ChannelMissingSettingError):
        await RC.connect()
        
@pytest.mark.asyncio
async def test_redis_channel_disconnect_valid() -> None:
    redis_client = aioredis.Redis()
    
    RC = RedisChannel()
    RC.r = redis_client
    RC._pubsub = redis_client.pubsub()
    await RC.disconnect()
    
    assert RC.r == None
    assert RC.pipeline == None
    assert RC._pubsub == None
    
@pytest.mark.asyncio  
async def test_redis_channel_disconnect_invalid_empty() -> None:     
    RC = RedisChannel()
    with pytest.raises(ChannelMissingSettingError):
        await RC.disconnect()

# ---- Function calls ----
@pytest.mark.asyncio  
async def test_redis_channel_broadcast_valid(redis_client) -> None:
    redis_client.from_url("redis://localhost:16379")
    
    RC = RedisChannel()
    RC.r = redis_client
    RC.host_name = {'URL': "redis://localhost:16379"}
    RC.out_streams = ["processed_data"]
    RC.in_streams = ["mkt_data:cqg", "mkt_data:fix"]
    RC.last_ids = {"mkt_data:cqg": "$", "mkt_data:fix": "$"}

    parsed_msg = ('1', 2, 3.0, True)
    byte_msg = msgpack.packb(parsed_msg)
    await RC.broadcast(parsed_msg, "processed_data")
    data = await redis_client.xread(streams={"processed_data": "0"}, count=1)
    assert data[0][1][0][1][b'data'] == byte_msg
    
@pytest.mark.asyncio  
async def test_redis_channel_broadcast_invalid_no_redis() -> None:
    RC = RedisChannel()

    parsed_msg = ('1', 2, 3.0, True)
    with pytest.raises(ChannelMissingSettingError):
        await RC.broadcast(parsed_msg, "processed_data")
        
@pytest.mark.asyncio  
async def test_redis_channel_broadcast_invalid_exception(redis_client) -> None:
    redis_client.from_url("redis://localhost:16379")
    
    RC = RedisChannel()
    RC.r = redis_client
    RC.host_name = {'URL': "redis://localhost:16379"}
    RC.out_streams = ["processed_data"]
    RC.in_streams = ["mkt_data:cqg", "mkt_data:fix"]
    RC.last_ids = {"mkt_data:cqg": "$", "mkt_data:fix": "$"}
    
    unpacked_msg = (object(),)
    with pytest.raises(ChannelBroadcastError):
        await RC.broadcast(unpacked_msg, "processed_data") #<--non -existent stream
        

@pytest.mark.asyncio      
async def test_redis_channel_listen_valid(redis_client) -> None:
    RC = RedisChannel()
    RC.r = redis_client
    RC.host_name = {'URL': "redis://localhost:16379"}
    RC.out_streams = ["processed_data"]
    RC.in_streams = ["mkt_data:cqg", "mkt_data:fix"]
    RC.last_ids = {"mkt_data:cqg": "0", "mkt_data:fix": "0"}

    parsed_msg = ('1', 2, 3.0, True)
    # Not that the b'data' here is intensionaly because msgpack send only bytes
    await RC.r.xadd("mkt_data:cqg", {b'data': msgpack.packb(parsed_msg)})
    await asyncio.sleep(0)
    
    data = await RC.listen("mkt_data:cqg",'data')
    assert RC.last_ids

    assert data == parsed_msg
    
@pytest.mark.asyncio      
async def test_redis_channel_listen_invalid_no_redis() -> None:
    RC = RedisChannel()
    with pytest.raises(ChannelMissingSettingError):
        await RC.listen('stream_name')
    
@pytest.mark.asyncio      
async def test_redis_channel_listen_invalid_no_last_ids(redis_client) -> None:
    RC = RedisChannel()
    RC.r = redis_client

    with pytest.raises(ChannelMissingSettingError):
        await RC.listen('stream_name')
 
@pytest.mark.asyncio      
async def test_redis_channel_listen_invalid_exceed_one_listener(redis_client) -> None:
    RC = RedisChannel()
    RC.r = redis_client
    RC.host_name = {'URL': "redis://localhost:16379"}
    RC.out_streams = ["processed_data"]
    RC.in_streams = ["mkt_data:cqg", "mkt_data:fix"]
    RC.last_ids = {"mkt_data:cqg": "0", "mkt_data:fix": "0"}
    
    RC._active_listeners.add("mkt_data:cqg")
    
    with pytest.raises(ChannelListenError):
        await RC.listen("mkt_data:cqg")

@pytest.mark.asyncio      
async def test_redis_channel_listen_invalid_empty_msg(redis_client) -> None:
    RC = RedisChannel()
    RC.r = redis_client
    RC.xread_block = 100
    RC.host_name = {'URL': "redis://localhost:16379"}
    RC.out_streams = ["processed_data"]
    RC.in_streams = ["mkt_data:cqg", "mkt_data:fix"]
    RC.last_ids = {"mkt_data:cqg": "0", "mkt_data:fix": "0"}

    #parsed_msg = ('1', 2, 3.0, True)
    # Not that the b'data' here is intensionaly because msgpack send only bytes
    #await RC.r.xadd("mkt_data:cqg", {b'data': msgpack.packb(parsed_msg)})
    #await asyncio.sleep(5)
    
    data = await RC.listen("mkt_data:cqg",'data')
    await asyncio.sleep(0.1)
    assert data is None
    
@pytest.mark.asyncio
async def test_redis_channel_listen_invalid_bad_data(redis_client) -> None:
    RC = RedisChannel()
    RC.r = redis_client
    RC.last_ids = {"mkt_data:cqg": "0"}

    await redis_client.xadd("mkt_data:cqg", {b"data": b"\xff\xff\xff"})  # not valid msgpack

    with pytest.raises(ChannelListenError):
        await RC.listen("mkt_data:cqg")
