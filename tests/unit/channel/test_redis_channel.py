#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:52:59 2026

@author: dexter
"""

from pathlib import Path
import pytest
import redis
import redis.asyncio as aioredis
from EC_API.channel.redis import RedisChannel
from EC_API.exceptions import (
    ConfigInputError, 
    ConfigFormatError,
    ChannelMissingSettingError
    )

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"
TEST_TOML_TCP_SOCKET = FIXTURES_DIR / "test_redis_channel_setup_tcp_socket.toml"
TEST_TOML_UDS = FIXTURES_DIR / "test_redis_channel_setup_UDS.toml"

BAD_CONFIGS = [
    # (toml_bytes, expected_exception)
    (b"this is not valid toml ===",
ConfigInputError),
    (b'[streams]\nin_streams = ["s1"]',
ConfigFormatError),  # no host_name
    (b'[host_name]\nURL = "redis://localhost:6379"',
ConfigFormatError),  # no streams
    (b'[host_name]\nURL = "redis://localhost:6379"\n[streams]',
ConfigFormatError),  # streams empty
]


def test_redis_channel_load_valid() -> None:
    RC = RedisChannel()
    RC.load(TEST_TOML_TCP_SOCKET)
    assert RC.host_name['URL'] == "redis://localhost:16379"
    assert RC.in_streams == ["mkt_data:cqg", "mkt_data:fix"]
    assert RC.out_streams == ["processed_data"]
    assert list(RC.last_ids.keys()) == ["mkt_data:cqg", "mkt_data:fix"]
    assert list(RC.last_ids.values()) == ["$", "$"]
    
@pytest.mark.parametrize("content, exc", BAD_CONFIGS)
def test_redis_channel_load_invalid_config(tmp_path, content, exc):
    f = tmp_path / "config.toml"
    f.write_bytes(content)
    with pytest.raises(exc):
        RedisChannel(path=str(f))

def test_redis_channel_load_invalid_missing_file():
    with pytest.raises(ConfigInputError):
        RedisChannel(path="/nonexistent/config.toml")
        
def test_redis_channel_connect_valid() -> None:
    RC = RedisChannel(TEST_TOML_TCP_SOCKET)
    RC.connect()
    assert isinstance(RC.r, aioredis.Redis)
    assert isinstance(RC.pipeline, aioredis.client.Pipeline)
    assert isinstance(RC._pubsub, aioredis.client.PubSub)
    
def test_redis_channel_connect_invalid_hostname_empty() -> None:
    RC = RedisChannel()
    with pytest.raises(ChannelMissingSettingError):
        RC.connect()
        
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



