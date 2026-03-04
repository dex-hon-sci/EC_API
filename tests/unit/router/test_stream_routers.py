#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 28 01:33:13 2026

@author: dexter
"""
import asyncio
import pytest
from EC_API.transport.routers import StreamRouter
from EC_API.exceptions import (
    SubscriptionQueueMismatchError,
    UnknownSubscriptionError
)

def test_subscribe_valid() -> None:
    SR = StreamRouter()
    SR.subscribe(1)
    SR.subscribe(1)
    SR.subscribe(1)
    assert len(SR._subs) == 1
    assert len(SR._subs[1]) == 3
    
    for i in range(3):
        assert isinstance(SR._subs[1][i], asyncio.Queue)
        
def test_unsubscribe_valid() -> None: 
    SR = StreamRouter()
    q1_1 = SR.subscribe(1)
    q1_2 = SR.subscribe(1)
    q2 = SR.subscribe(2)
    
    SR.unsubscribe(1, q1_1)
    assert len(SR._subs) == 2
    assert len(SR._subs[1]) == 1
    assert len(SR._subs[2]) == 1
    assert isinstance(SR._subs[1][0], asyncio.Queue)
    assert isinstance(SR._subs[2][0], asyncio.Queue)

def test_unsubscribe_invalid_q() -> None:
    SR = StreamRouter()
    q1_1 = SR.subscribe(1)
    q1_2 = SR.subscribe(1)
    q2 = SR.subscribe(2)
    with pytest.raises(SubscriptionQueueMismatchError) as e:
        SR.unsubscribe(1, q2)
         
    assert len(SR._subs[1]) == 2
    assert len(SR._subs[2]) == 1
    
def test_unsubscribe_removes_empty_contract_entry():
    SR = StreamRouter()
    q = SR.subscribe(1)
    SR.unsubscribe(1,q)
    assert 1 not in SR._subs
    
@pytest.mark.asyncio
async def test_publish_valid() -> None:
    SR = StreamRouter()
    q1_1 = SR.subscribe(1)
    q1_2 = SR.subscribe(1)
    q2 = SR.subscribe(2)
    
    content = [(1,1), (1,2), (2,1), (2,2), (1,3), (1,4),
               (1,5), (1,6), (2,3), (1,7), (1,8), (2,4)]
    for c in content:
        await SR.publish(c[0], c, cool_time=0)
        
    assert isinstance(SR._subs[1][0], asyncio.Queue)
    assert isinstance(SR._subs[1][1], asyncio.Queue)
    assert isinstance(SR._subs[2][0], asyncio.Queue)
    assert SR._subs[1][0].qsize() == 8
    assert SR._subs[1][1].qsize() == 8
    assert SR._subs[2][0].qsize() == 4
    
    expected_1 = [c for c in content if c[0] == 1]
    expected_2 = [c for c in content if c[0] == 2]

    out_1_1 = [q1_1.get_nowait() for _ in range(q1_1.qsize())]
    out_1_2 = [q1_2.get_nowait() for _ in range(q1_2.qsize())]
    out_2   = [q2.get_nowait()   for _ in range(q2.qsize())]

    assert out_1_1 == expected_1
    assert out_1_2 == expected_1
    assert out_2 == expected_2

@pytest.mark.asyncio
async def test_drop_drop_if_full_drop_oldest_valid() -> None:
    SR = StreamRouter(max_queue_size=5, drop_if_full=True, drop_policy="drop_oldest")
    q1 = SR.subscribe(1)
    
    content = [(1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)]

    for c in content:
        await SR.publish(1, c,cool_time=0)
    
    assert SR._subs[1][0].qsize() == 5
    out = [q1.get_nowait() for _ in range(q1.qsize())]
    assert out == content[-5:]

@pytest.mark.asyncio
async def test_publish_no_subscribers_noop():
    SR = StreamRouter()
    before = dict(SR._subs)    
    await SR.publish(999, ("x",), cool_time=0)  # should not raise
    assert SR._subs == before