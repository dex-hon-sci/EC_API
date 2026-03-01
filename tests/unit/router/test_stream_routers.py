#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 01:33:13 2026

@author: dexter
"""
import asyncio
import pytest
from EC_API.transport.routers import StreamRouter

@pytest.mark.asyncio
async def test_subscribe_valid() -> None:
    SR = StreamRouter()
    SR.subscribe(1)
    SR.subscribe(1)
    SR.subscribe(1)
    print(SR._subs)
    assert len(SR._subs) == 1
    assert len(SR._subs[1]) == 3
    
    for i in range(3):
        assert isinstance(SR._subs[1][i], asyncio.Queue)
        
@pytest.mark.asyncio
async def test_unsubscribe_valid() -> None: 
    SR = StreamRouter()
    q1_1 = SR.subscribe(1)
    q1_2 = SR.subscribe(1)
    q2 = SR.subscribe(2)
    
    SR.unsubscribe(1, q1_1)
    assert len(SR._subs[1]) == 1
    assert len(SR._subs[2]) == 1
    assert isinstance(SR._subs[1][0], asyncio.Queue)
    assert isinstance(SR._subs[2][0], asyncio.Queue)

@pytest.mark.asyncio
async def test_unsubscribe_invalid_q() -> None:
    SR = StreamRouter()
    q1_1 = SR.subscribe(1)
    q1_2 = SR.subscribe(1)
    q2 = SR.subscribe(2)
    
    SR.unsubscribe(1, q2)
    assert len(SR._subs[1]) == 2
    
@pytest.mark.asyncio
async def test_publish_valid() -> None:
    ...

@pytest.mark.asyncio
async def test_drop_if_full_valid() -> None:
     SR = StreamRouter(max_queue_size=5)
     

    
