#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 18:38:26 2025

@author: dexter
"""
# In the Future we need a Strategy scanner machine that check compliance of 
# a strategy, for example, scan if the strategy action tree ultimately 
# have an equal qty of Buy/Sell orders (balance check).


import pytest
import asyncio
# Setup dummu live-data
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from EC_API.monitor.tick import TimeTickBuffer
from EC_API.monitor.data_feed import DataFeed
from EC_API.op_strategy.action import ActionContext
from tests.example_actiontree import tree as ACTION_TREE

# Trigger Conditions
# a, b, c, d, a2 = 100, 50, 60, 70, 80

@dataclass
class IncomingTicks:
    def __init__(self, prices: list[float|int]):
        self.prices  = prices #[10,40,70,20]
        self.volumes: list[float|int] = [4,1,10,4]
        self.timestamps: list[float] = [
                    datetime.now(tz=timezone.utc).timestamp(),
                    (datetime.now()+timedelta(seconds=1)).timestamp(),
                    (datetime.now()+timedelta(seconds=2)).timestamp(),
                    (datetime.now()+timedelta(seconds=3)).timestamp(),
                    ]
        self._feed = None
        
    @property
    def feed(self):
        self._feed = zip(self.prices,
                        self.volumes,
                        self.timestamps)
        return self._feed
    
@pytest.mark.asyncio       
async def test_action_sequence_TP1() -> None:
    IT = IncomingTicks([101,40,70,20])
    TB = TimeTickBuffer([60])
    DF = DataFeed(TB, symbol="Asset_A")
    ctx = ActionContext(feeds = {"Asset_A": DF})

    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        print("+++++ current tickbuf [", DF.tick_buffer.ohlc()['Close'], "]")
        print("++++ current ctx df [", ctx.feeds["Asset_A"].tick_buffer.ohlc()['Close'],"]")
        print('+++++'+ACTION_TREE.cur.label+'+++++:',ACTION_TREE.cur.status)
        print("Payload:", ACTION_TREE.cur.payloads[0].request_id)
        await ACTION_TREE.step(ctx)
        
    # Select * in DB and check if the Payloads matches
        
    
def test_action_sequence_mod_TP2() -> None:
    pass

def test_action_sequence_cancel() -> None:
    IT = IncomingTicks([101,90,70,20])
    TB = TimeTickBuffer([60])
    DF = DataFeed(TB, symbol="Asset_A")
    ctx = ActionContext(feeds = {"Asset_A": DF})

    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        print("+++++ current tickbuf [", DF.tick_buffer.ohlc()['Close'], "]")
        print("++++ current ctx df [", ctx.feeds["Asset_A"].tick_buffer.ohlc()['Close'],"]")
        print('+++++'+ACTION_TREE.cur.label+'+++++:',ACTION_TREE.cur.status)
        print("Payload:", ACTION_TREE.cur.payloads[0].request_id)
        await ACTION_TREE.step(ctx)
        

def test_action_sequence_overtime() -> None:
    pass

def test_() -> None:
    pass

print("====Test Started =====")
asyncio.run(test_action_sequence_TP1())