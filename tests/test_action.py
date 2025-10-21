#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 18:38:26 2025

@author: dexter
"""
# In the Future we need a Strategy scanner machine that check compliance of 
# a strategy, for example, scan if the strategy action tree ultimately 
# have an equal qty of Buy/Sell orders (balance check).


from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import pytest
import pytest_asyncio
import asyncio
from sqlalchemy import select, delete
from EC_API.monitor.tick import TimeTickBuffer
from EC_API.monitor.data_feed import DataFeed
from EC_API.op_strategy.action import ActionContext
from EC_API.ordering.enums import RequestType, OrderType, Side
from tests.example_actiontree import tree as ACTION_TREE
from tests.example_db import (
    init_db, engine, Base, TEST_ASYNC_SESSION, TestStorage
    )

@dataclass
class IncomingTicks: # Setup dummy live-data
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
    
async def actionflow_validation(prices: list[float]) -> None:
    # A function that first go through the Action flow chart, and 
    # check the DB entries for validation
    # Define the answers for this test

    # DataFeed setup
    IT = IncomingTicks(prices)
    TB = TimeTickBuffer([60])
    DF = DataFeed(TB, symbol="Asset_A")
    ctx = ActionContext(feeds = {"Asset_A": DF})

    for price, volume, timestamp in IT.feed:
        print('---------------------------------------------')
        DF.tick_buffer.add_tick(price, volume, timestamp)
        print("+++++ current tickbuf [", DF.tick_buffer.ohlc()['Close'], "]")
        print("++++ current ctx df [", ctx.feeds["Asset_A"].tick_buffer.ohlc()['Close'],"]")
        print('+++++'+ACTION_TREE.cur.label+'+++++:',ACTION_TREE.cur.status)
        print("Payload:", ACTION_TREE.cur.payloads[0].request_id)
        await ACTION_TREE.step(ctx)
        
    # Select * in DB and check if the Payloads matches
    async with TEST_ASYNC_SESSION() as session:
        entries = await session.execute(select(TestStorage))
        
    entries_list = entries.scalars().all()
    return entries_list

#############
# Constants
price_a_up, price_a1, price_b, price_c, price_d, price_a2 = 105, 100, 50, 60, 40, 80
price_a, price_b1, price_b2, price_c2, price_d2, price_e3 = 105, 100, 50, 60, 40, 80

# Route 1
TP1test_prices = [101,40,70,20]
TP1test_answer_ids = (100, 103)
TP1test_answer_sides = (Side.SIDE_SELL, Side.SIDE_BUY)
TP1test_answer_rq_types = (OrderType.ORDER_TYPE_LMT, OrderType.ORDER_TYPE_LMT)
TP1test_answer_qtys =  (2, 2)
TP1test_answer_LMT_price =  (price_a1, price_c)

# Route 2
TP2test_prices = [102, 80, 58, 55, 57, 40, 38]
TP2test_answer_ids = (100, 102, 104)
TP2test_answer_sides = (Side.SIDE_SELL, Side.SIDE_SELL, Side.SIDE_BUY)
TP2test_answer_rq_types = (OrderType.ORDER_TYPE_LMT, OrderType.ORDER_TYPE_LMT,
                           OrderType.ORDER_TYPE_LMT)
TP2test_answer_qtys =  (2, 2, 2)
TP2test_answer_LMT_price =  (price_a1, price_a2, price_d)

# Route 3

# Route 4


@pytest.mark.asyncio    
async def test_action_sequence_TP1() -> None:
    # Initialise DB
    await init_db()

    entries_list = await actionflow_validation(TP1test_prices)
    
    for i, ele in enumerate(entries_list):
        assert ele.request_id == TP1test_answer_ids[i]
        assert ele.order_info["order_type"] == TP1test_answer_rq_types[i]
        assert ele.order_info["qty_significant"] == TP1test_answer_qtys[i]
        assert ele.order_info["side"] == TP1test_answer_sides[i]
        assert ele.order_info["scaled_limit_price"] == TP1test_answer_LMT_price[i]
        
    # Delete all entry in DB
    async with TEST_ASYNC_SESSION() as session:
        await session.execute(delete(TestStorage))
        await session.commit()
        

@pytest.mark.asyncio    
async def test_action_sequence_mod_TP2() -> None:
    # Initialise DB
    await init_db()

    entries_list = await actionflow_validation(TP2test_prices)
    
    for i, ele in enumerate(entries_list):
        assert ele.request_id == TP2test_answer_ids[i]
        assert ele.order_info["order_type"] == TP2test_answer_rq_types[i]
        assert ele.order_info["qty_significant"] == TP2test_answer_qtys[i]
        assert ele.order_info["side"] == TP2test_answer_sides[i]
        assert ele.order_info["scaled_limit_price"] == TP2test_answer_LMT_price[i]

    # Delete all entry in DB
    #async with TEST_ASYNC_SESSION() as session:
    #    await session.execute(delete(TestStorage))
    #    await session.commit()
        
@pytest.mark.asyncio       
async def test_action_sequence_cancel() -> None:
    pass

@pytest.mark.asyncio       
async def test_action_sequence_overtime() -> None:
     pass


# =============================================================================
# @pytest.mark.asyncio       
# async def test_action_sequence_cancel() -> None:
#     IT = IncomingTicks([101,90,70,20])
#     TB = TimeTickBuffer([60])
#     DF = DataFeed(TB, symbol="Asset_A")
#     ctx = ActionContext(feeds = {"Asset_A": DF})
# 
#     for price, volume, timestamp in IT.feed:
#         DF.tick_buffer.add_tick(price, volume, timestamp)
#         print("+++++ current tickbuf [", DF.tick_buffer.ohlc()['Close'], "]")
#         print("++++ current ctx df [", ctx.feeds["Asset_A"].tick_buffer.ohlc()['Close'],"]")
#         print('+++++'+ACTION_TREE.cur.label+'+++++:',ACTION_TREE.cur.status)
#         print("Payload:", ACTION_TREE.cur.payloads[0].request_id)
#         await ACTION_TREE.step(ctx)
# =============================================================================
        
print("====Test Started =====")
#asyncio.run(test_action_sequence_TP1())
asyncio.run(test_action_sequence_mod_TP2())