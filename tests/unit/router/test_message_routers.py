#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:56:37 2026

@author: dexter
"""
import asyncio
import pytest
from EC_API.transport.routers import MessageRouter

@pytest.mark.asyncio
async def test_key_register_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)
    
    assert len(MR._pending) == 2
    assert list(MR._pending.keys())[0] == key1
    assert list(MR._pending.keys())[1] == key2
    assert isinstance(fut1, asyncio.Future)
    assert isinstance(fut2, asyncio.Future)    
    assert MR._pending[key1].done() == False
    assert MR._pending[key2].done() == False
    
@pytest.mark.asyncio
async def test_on_message_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)

    MR.on_message(key1, {"Message_1": "Content_1"})
    assert len(MR._pending) == 1
    assert fut1.done() is True
    res1 = await asyncio.wait_for(fut1, timeout=1.0)
    assert res1 ==  {"Message_1": "Content_1"}
    
    MR.on_message(key2, {"Message_2": "Content_2"})
    assert MR._pending == {}
    assert fut2.done() is True
    res2 = await asyncio.wait_for(fut2, timeout=1.0)
    assert res2 ==  {"Message_2": "Content_2"}       
  
@pytest.mark.asyncio 
async def test_fail_all_valid() -> None:
    key1 = ("msg_family_1", "msg_type_A", "request_id", 12)
    key2 = ("msg_family_2", "msg_type_B", "id", "id_1")
    
    MR = MessageRouter()
    fut1 = MR.register_key(key1)
    fut2 = MR.register_key(key2)
    
    exc = RuntimeError("connection lost")
    MR.fail_all(exc)
    
    assert fut1.done()
    assert fut2.done()
    
    with pytest.raises(RuntimeError, match="connection lost"):
        await fut1

    with pytest.raises(RuntimeError, match="connection lost"):
        await fut2

    assert MR._pending == {}

