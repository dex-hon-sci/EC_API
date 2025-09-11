#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:40:47 2025

@author: dexter
"""
from datetime import datetime, timedelta
import pytest
from EC_API.monitor.tick import TickBuffer
from EC_API.monitor.data_feed import DataFeed


class IncomingTicks:
    def __init__(self):
        self.pirces: list[float|int] = [10,40,70,20]
        self.volumes: list[float|int] = [4,1,10,4]
        self.timestamps: list[float] = [
                            datetime.now().timestamp(),
                            (datetime.now()+timedelta(seconds=1)).timestamp(),
                            (datetime.now()+timedelta(seconds=2)).timestamp(),
                            (datetime.now()+timedelta(seconds=3)).timestamp(),
                            ]
        
        self.feed = zip(self.pirces,
                        self.volumes,
                        self.timestamps)
        
def test_addto_tickbuffer() -> None:
    IT = IncomingTicks()
    
    TB = TickBuffer([60])
    DF = DataFeed(TB, symbol="AddtoTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
    
    for index, tick in enumerate(DF.tick_buffer.buffers.get(60)):
        assert tick.price == IT.pirces[index]
        assert tick.volume == IT.volumes[index]
        assert tick.timestamp < IT.timestamps[index] + 1e-4
        assert tick.timestamp > IT.timestamps[index] - 1e-4
        
def test_popleft_tickbuffer() -> None:
    IT = IncomingTicks()

    IT.timestamps = [datetime.now().timestamp(),
                    (datetime.now()+timedelta(seconds=10.1)).timestamp(),
                    (datetime.now()+timedelta(seconds=20.1)).timestamp(),
                    (datetime.now()+timedelta(seconds=30.1)).timestamp(),
                    ] # Evict ticks every iteration
    print("IT.timestamps", IT.timestamps)
    print("Input", [datetime.now().timestamp(),
                    (datetime.now()+timedelta(seconds=10.1)).timestamp(),
                    (datetime.now()+timedelta(seconds=20.1)).timestamp(),
                    (datetime.now()+timedelta(seconds=30.1)).timestamp(),
                    ])
    
    TB = TickBuffer([10])
    DF = DataFeed(TB, symbol="PopLeftTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        #print(price, volume, timestamp)
        #print(DF.tick_buffer.buffers.get(10))
        assert len(DF.tick_buffer.buffers.get(10)) == 1
        assert DF.tick_buffer.buffers.get(10)[0].price == price
        assert DF.tick_buffer.buffers.get(10)[0].volume == volume
        assert DF.tick_buffer.buffers.get(10)[0].timestamp == timestamp
        
test_popleft_tickbuffer()
def test_multi_timeframe_tickbuffer() -> None:
    incoming_ticks_pirce = [10,40,70,20]
    incoming_ticks_volume = [4,1,10,4]
    incoming_ticks_timestamp = [datetime.now().timestamp(),
                                (datetime.now()+timedelta(seconds=10)).timestamp(),
                                (datetime.now()+timedelta(seconds=20)).timestamp(),
                                (datetime.now()+timedelta(seconds=30)).timestamp(),
                                ] # Evict ticks every iteration

    TB = TickBuffer([10, 20, 30])
    DF = DataFeed(TB, symbol="Multi-TimeFrame")
    
    feed = zip(incoming_ticks_pirce, 
               incoming_ticks_volume, 
               incoming_ticks_timestamp, 
               )
    

def test_update_tickbuffer_stat_all() -> None:
    pass

def test_update_tickbuffer_stat_selection() -> None:
    pass