#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 18:38:26 2025

@author: dexter
"""
# In the Future we need a Strategy scanner machine that check compliance of 
# a strategy, for example, scan if the strategy action tree ultimately 
# have an equal qty of Buy/Sell orders (balance check).



# Setup dummu live-data
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from EC_API.monitor.tick import TimeTickBuffer
from EC_API.monitor.data_feed import DataFeed
from tests.example_actiontree import tree

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
        

def test_action_sequence_TP1() -> None:
    IT = IncomingTicks([10,40,70,20])
    TB = TimeTickBuffer([60])
    DF = DataFeed(TB, symbol="Asset_A")
    
def test_action_sequence_mod_TP2() -> None:
    pass

def test_action_sequence_cancel() -> None:
    pass

def test_action_sequence_overtime() -> None:
    pass

def test_() -> None:
    pass
