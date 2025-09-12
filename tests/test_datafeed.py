#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 09:40:47 2025

@author: dexter
"""
# Python Imports
from dataclasses import dataclass
from datetime import datetime, timedelta
# Pyhton Package imports
import pytest
# EC_API imports
from EC_API.monitor.tick import TickBuffer
from EC_API.monitor.tick_stats import TickBufferStat, ALL_STATS
from EC_API.monitor.data_feed import DataFeed

@dataclass
class IncomingTicks:
    def __init__(self):
        self.prices: list[float|int] = [10,40,70,20]
        self.volumes: list[float|int] = [4,1,10,4]
        self.timestamps: list[float] = [
                    datetime.now().timestamp(),
                    (datetime.now()+timedelta(seconds=10)).timestamp(),
                    (datetime.now()+timedelta(seconds=20)).timestamp(),
                    (datetime.now()+timedelta(seconds=30)).timestamp(),
                    ]
        self._feed = None
        
    @property
    def feed(self):
        self._feed = zip(self.prices,
                        self.volumes,
                        self.timestamps)
        return self._feed
        
def test_addto_tickbuffer() -> None:
    IT = IncomingTicks()
    TB = TickBuffer([60])
    DF = DataFeed(TB, symbol="AddtoTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
    
    for index, tick in enumerate(DF.tick_buffer.buffers.get(60)):
        assert tick.price == IT.prices[index]
        assert tick.volume == IT.volumes[index]
        assert tick.timestamp < IT.timestamps[index] + 1e-4
        assert tick.timestamp > IT.timestamps[index] - 1e-4
        
def test_popleft_tickbuffer() -> None:
    IT = IncomingTicks()
    IT.timestamps = [datetime.now().timestamp(),
                    (datetime.now()+timedelta(seconds=10.2)).timestamp(),
                    (datetime.now()+timedelta(seconds=20.2)).timestamp(),
                    (datetime.now()+timedelta(seconds=30.2)).timestamp(),
                    ] # Evict ticks every iteration

    TB = TickBuffer([10])
    DF = DataFeed(TB, symbol="PopLeftTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        #print(len(DF.tick_buffer.buffers.get(10)))
        #print(DF.tick_buffer.buffers.get(10))
        assert len(DF.tick_buffer.buffers.get(10)) == 1
        assert DF.tick_buffer.buffers.get(10)[0].price == price
        assert DF.tick_buffer.buffers.get(10)[0].volume == volume
        assert DF.tick_buffer.buffers.get(10)[0].timestamp == timestamp
        
def test_multi_timeframe_tickbuffer() -> None:
    IT = IncomingTicks()
    IT.timestamps = [datetime.now().timestamp(),
                    (datetime.now()+timedelta(seconds=8.9)).timestamp(),
                    (datetime.now()+timedelta(seconds=18.9)).timestamp(),
                    (datetime.now()+timedelta(seconds=28.9)).timestamp(),
                    ] # Evict ticks every iteration
    timeframe = [10, 20, 30]
    len_seq = {10:[1,2,1,1], 20:[1,2,3,2], 30:[1,2,3,4]}
    # first step: len_10 = 1, len_20 = 1, len_30 = 1;
    # second step: len_10 =2, len_20 = 2, len_30 = 2;
    # third step: len_10 =1, len_20 = 3, len_30 = 3;
    # fourth step: len_10 =1, len_20 = 2, len_30 = 4;

    TB = TickBuffer(timeframe)
    DF = DataFeed(TB, symbol="Multi-TimeFrame")
    index = 0
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        #print('---------------------')
        for num in timeframe:
            #print(num, len(DF.tick_buffer.buffers.get(num)), len_seq.get(num)[index])
            #print(DF.tick_buffer.buffers.get(num))
            assert DF.tick_buffer.buffers.get(num)
            assert len(DF.tick_buffer.buffers.get(num)) == len_seq.get(num)[index]
        index+=1

def test_update_tickbuffer_stat_all() -> None:
    IT = IncomingTicks()
    TB = TickBuffer([50]) # include all entries
    DF = DataFeed(TB, symbol="Stat_all")
        #self.prices: list[float|int] = [10,40,70,20]
        #self.volumes: list[float|int] = [4,1,10,4]

    mean_price = [10,25,40,35]
    std_price = [0.0, 21.2132034, 30.0, 26.457513110]
    ohlc_price = [{"open":10, "high":10, "low":10, "close":10},
            {"open":10, "high":40, "low":10, "close":40},
            {"open":10, "high":70, "low":10, "close":70},
            {"open":10, "high":70, "low":10, "close":20},
            ]
    mean_volume = [4.0,2.5,5.0,4.75]
    std_volume = [0.0, 2.1213203, 4.58257569, 3.77491721]
    vwap = [10.0, 16.0, 52.0, 45.2631578]
    
    zip_all = zip(mean_price, std_price, ohlc_price, mean_volume, std_volume, vwap)
    
    stat_all_answers = [{"mean_price": mean_p,
                         "std_price": std_p,
                         "ohlc_price":ohlc,
                         "mean_volume": mean_v,
                         "std_volume": std_v,
                         "vwap": vwap
                         } for mean_p, std_p, 
                               ohlc, mean_v, 
                               std_v, vwap in zip_all]
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(price, volume, timestamp)
        stats = DF.tick_buffer_stat # call stat method

        

def test_update_tickbuffer_stat_selection() -> None:
    pass