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
import numpy as np
# EC_API imports
from EC_API.monitor.tick import TimeTickBuffer
from EC_API.monitor.tick_stats import TickBufferStat
from EC_API.monitor.stat_metrics import (
    VWAP, OHLC, 
    MeanPrice, MeanVolume, 
    StdPrice, StdVolume
    )
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
    TB = TimeTickBuffer([60])
    DF = DataFeed(TB, symbol="AddtoTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(timestamp, price, volume)
    
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

    TB = TimeTickBuffer([10])
    DF = DataFeed(TB, symbol="PopLeftTest")
    
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(timestamp, price, volume)
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

    TB = TimeTickBuffer(timeframe)
    DF = DataFeed(TB, symbol="Multi-TimeFrame")
    index = 0
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(timestamp, price, volume)
        #print('---------------------')
        for num in timeframe:
            #print(num, len(DF.tick_buffer.buffers.get(num)), len_seq.get(num)[index])
            #print(DF.tick_buffer.buffers.get(num))
            assert DF.tick_buffer.buffers.get(num)
            assert len(DF.tick_buffer.buffers.get(num)) == len_seq.get(num)[index]
        index+=1

def test_update_tickbuffer_stat_all() -> None:
    IT = IncomingTicks()
    TB = TimeTickBuffer([50]) # include all entries
    DF = DataFeed(TB, 
                  #buf_stat_method=TBS,
                  calculators = {
                        "mean_price": MeanPrice(),
                        "std_price": StdPrice(),
                        "ohlc_price": OHLC(),
                        "mean_volume": MeanVolume(),
                        "std_volume": StdVolume(),
                        "vwap": VWAP()
                        },
                  min_n = 1,
                  symbol="Stat_all")

    mean_price = [10,25,40,35]
    std_price = [np.nan, 21.2132034, 30.0, 26.457513110]
    ohlc_price = [
        {"open":10, "high":10, "low":10, "close":10},
        {"open":10, "high":40, "low":10, "close":40},
        {"open":10, "high":70, "low":10, "close":70},
        {"open":10, "high":70, "low":10, "close":20},
        ]
    mean_volume = [4.0,2.5,5.0,4.75]
    std_volume = [np.nan, 2.1213203, 4.58257569, 3.77491721]
    vwap = [10.0, 16.0, 52.0, 45.2631578]
    
    zip_all = zip(mean_price, std_price, ohlc_price, mean_volume, std_volume, vwap)
    
    stat_all_answers = [{"n": i +1,
                         "mean_price": mean_p,
                         "std_price": std_p,
                         "ohlc_price":ohlc,
                         "mean_volume": mean_v,
                         "std_volume": std_v,
                         "vwap": vwap
                         } for i, (mean_p, std_p, 
                               ohlc, mean_v, 
                               std_v, vwap) in enumerate(zip_all)]
    delta = 1e-5
    index = 0 
    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(timestamp, price, volume)
        #print("Add tick complete")
        stats = DF.tick_buffer_stat(timestamp-50, timestamp) # call stat method
        #print("stats", stats)
        for stat_ele in stats:
            answer = stat_all_answers[index][stat_ele]
            print("stat_ele", stat_ele, stats[stat_ele], answer)

            if stat_ele == "ohlc_price":
                assert stats[stat_ele]['open'] == answer['open']
                assert stats[stat_ele]['high'] == answer['high']
                assert stats[stat_ele]['low'] == answer['low']
                assert stats[stat_ele]['close'] == answer['close']
            elif stat_ele == 'n':
                assert stats[stat_ele] == answer
            elif answer is np.nan:
                assert np.isnan(stats[stat_ele])
            else:
                assert stats[stat_ele] < answer + delta
                assert stats[stat_ele] > answer - delta
        index += 1

def test_update_tickbuffer_stat_selection() -> None:
    IT = IncomingTicks()
    TB = TimeTickBuffer([50]) # include all entries
    #print('--creating DataFeed')
    DF = DataFeed(TB, 
                  calculators ={'mean_price':MeanPrice()}, 
                  min_n=1, 
                  symbol="Stat_selection")
    
    mean_price = [10,25,40,35]
    index = 0
    #print('--Running DataStream')

    for price, volume, timestamp in IT.feed:
        DF.tick_buffer.add_tick(timestamp, price, volume)
        stats = DF.tick_buffer_stat(timestamp-50, timestamp) # call stat method
        assert stats['n'] == index +1
        assert stats['mean_price'] == mean_price[index]
        index +=1
#test_update_tickbuffer_stat_all()
#test_update_tickbuffer_stat_selection()
#test_addto_tickbuffer()
# =============================================================================
# import time
# t1 = time.time()
# for i in range(300):
#     print(i)
#     test_update_tickbuffer_stat_all()
#     
# t2 = time.time() - t1
# print("time2", t2)
# =============================================================================
