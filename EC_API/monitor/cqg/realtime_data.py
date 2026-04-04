#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:06:40 2025

@author: dexter
"""
import asyncio
from typing import Any, Iterator
import numpy as np
# Import EC_API scripts
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.base import Monitor
from EC_API.monitor.tick import TickBuffer
from EC_API.monitor.tick_stats import TickBufferStat
from EC_API.monitor.data_feed import DataFeed

from EC_API.transport.cqg.base import TransportCQG
from EC_API.transport.routers import MessageRouter
from EC_API.monitor.cqg.builders import(
    build_realtime_data_request_msg,
    build_reset_tracker_request_msg
    )
from EC_API.exceptions import (
    MsgBuilderError
    )
class SubMgr:
    def __init__(self):
        name2id_ref = dict()
        ids_states = dict()
        
    def add_name(name: str, sub_id: int | str):
        # Add symbol_name/chain_order_id 
        return
    
    def add_scale(name:str,scale:float):
        return 
    

class MonitorDataCQG(Monitor):
    def __init__(self, conn: ConnectCQG):
        self._conn = conn
        self._transport = conn._transport()

        self._loop = asyncio.get_running_loop()
        #self._transport = TransportCQG()
        self._stream_router = self._conn._stream_router
        self.timeout = 1
        
        self.sub_mgr = SubMgr()
        
    @property
    def conn(self):
        return self._conn

    def rid(self) -> int:
        return self.conn.rid()

    async def _resolve_symbol(self, symbol_name: str):
        # Get the metadata first
        contract_metadata = await self._conn.resolve_symbol(symbol_name)
        
        # Save the contract_id to subscription manager
        self.sub_mgr.add_name(symbol_name, 1)
        
    
    async def subscribe_mkt_data(self, symbol_name: str, level):
        ref, fut = dict(), None
        contract_id = ref[symbol_name]

        try:
            msg = build_realtime_data_request_msg(contract_id, self.rid(), level)
        except MsgBuilderError as e:
            return 
        q = await self._stream_router.subscribe(contract_id)

        self._transport.send(msg)
        
        # Response handling
        server_msg = await asyncio.wait_for(fut, timeout = self._timeout)
        return q
    
    async def unsubscribe_mkt_data(self, symbol_name) -> None:
        contract_id = self.sub_mgr.subs[symbol_name]
        try:
            msg = build_reset_tracker_request_msg(contract_id, self.rid())
        except MsgBuilderError as e:
            return 
        
        self._transport.send(msg)
        self._stream_router.unsubscribe(contract_id)

    async def stream(self, contract_id) -> Iterator[tuple[int]]:
        # check if the rounter has the id already
        q = await self._stream_router.subscribe(contract_id)

        
        yield
    


class MonitorRealTimeDataCQG(Monitor):
    
    def __init__(self, conn: ConnectCQG):
        self._conn = conn
        self._transport = conn._transport()
        
        self.syms_to_contract_ids = dict()
        self.timeout = 1
        
        self.sub_mgr = None
        
    async def resolve_symbol(self, symbol: str, request_id: int) -> None:
        # symbol Resolution
        msg = build_resolve_symbol_msg(symbol, request_id, subscribe=True)
        fut = self._conn._msg_router.register_key(("rpc", "", "request_id", request_id))
        await self._transport.send(msg)
        server_msg = await asyncio.wait_for(fut, timeout=1)
        return 
        
    async def _subscribe_mkt_data(
        self, contract_id: int, request_id: int, level
        ) -> None:

        msg = build_realtime_data_request_msg(contract_id, request_id, level)
        fut = self._conn._msg_router.register_key(("", request_id))
        await self._transport.send(msg)
        server_msg = await asyncio.wait_for(fut, timeout=1)
        return 
    
    async def _unsubscribe_mkt_data(
        self, contract_id: int, request_id: int
        ) -> None:
        msg = build_reset_tracker_request_msg(contract_id, request_id)
        fut = self._conn._msg_router.register_key(("", request_id))
        await self._transport.send(msg)
        server_msg = await asyncio.wait_for(fut, timeout=1)
        return 
    
    async def stream(self, contract_id: int, level):
        # check if they are in the stream router
        self._subscribe_mkt_data()
        # stream
        q = self._conn._market_data_stream_router.subscribe(contract_id)
        
        try:
            while True:
                md = await q.get()
                for data in md:
                    yield data # do parsing here
        finally:
            await self._unsubscribe_mkt_data()
            self._conn._market_data_stream_router.unsubscribe(contract_id)
            

class MonitorRealTimeDataCQG2(Monitor):
    def __init__(self, connection: ConnectCQG):
        self._conn = connection
        self._transport = self._conn._transport
        
        self._msg_id: int = 200 # just a starting number for message id
        self.symbols: set[str] = set()
        
        # Define client
        #self._client = webapi_client.WebApiClient()
        self._loop = asyncio.get_running_loop()
        #self._transport = CQGTransport()
        self._router = MessageRouter()
        
        self._contract_to_symbol: dict[int, str] = {}
        self._per_contract_queues: dict[int, asyncio.Queue] = {} # queue for storing recv msg sorted

        self.total_recv_cycle: int = 20
        self.total_send_cycle: int = 2
        self.recv_cycle_delay: int = 0
        self.send_cycle_delay: int = 0

    @property
    def conn(self):
        return self._conn
    
    def rid(self) -> int:
        return self.conn.rid()
    
    @property
    def per_contract_queue(self)-> dict :
        return self._per_contract_queue

    async def _fanout_loop(self): # Basically sorting
        # Put the latest tick into the right async queue (based on contract_id)
        while True:
            server_msg = await self._conn.tick_q.get()
            #tick = parse_realtime_tick(server_msg) 
            # function that translate tick into
            tick = None

            symbol = self._contract_to_symbol.get(tick.contract_id, "")
            tick.symbol = symbol

            q = self._per_contract_q.get(tick.contract_id)
            if q is not None:
                await q.put(tick)
        
    async def stream(self, contract_id: int):
        pass # Get the data


    ######################    
    
    
    async def resolve_symbol(self, 
                             symbol: str, 
                             msg_id: int,
                             contract_ids: dict[str, int],
                             contract_metadata: dict[str],
                             **kwargs
                             ) -> None:
        # Set up contract_id and metadata for references
        #for symbol in self.symbols:
        print("======================")
        print("realtime monitor:", symbol, msg_id, contract_ids, contract_metadata)
        print("realtime monitor2:", symbol not in contract_ids)
        if symbol not in contract_ids:
            result_msg = await self._conn.resolve_symbol_async(symbol, msg_id, **kwargs)
            print("resolve_sym_msg", result_msg)
            contract_ids[symbol] = result_msg.contract_id 
            contract_metadata[symbol] = result_msg

# =============================================================================
#             try:
#                 result_msg = self._connection.resolve_symbol(symbol, msg_id)
#                 print("resolve_sym_msg", result_msg)
#                 contract_ids[symbol] = result_msg.contract_id 
#                 contract_metadata[symbol] = result_msg.resolve_symbol(symbol, msg_id)
#             except:
#                 print("Encounter problem resolving symbol.")
# =============================================================================
        #await asyncio.sleep(1.2)
        

    async def request_realtime_data(self, 
                                    contract_id: int, 
                                    level: int = 1, 
                                    default: tuple[ float | int] = (np.nan, np.nan, np.nan)
                                    ) -> tuple[int, float, int]:
        # Two loop approach: Not the most sophisticated but will do for now.
        # Could Use continuous scrapping with a buffer. Send all requests, recv
        # msg, scrap them and bank them in our buffer. Then we post it on the TSDB
        
        # Send request msg and rev response, stop the func when we get the three
        # condition correct: 1) recv real_time_market_data, 2) right ID, 3) recv
        # quote data.
        for attempt in range(self.total_send_cycle):
            client_msg = build_realtime_data_request_msg(contract_id,
                                                         self.msg_id,
                                                         level)

# =============================================================================
#             client_msg = ClientMsg()
#             subscription = client_msg.market_data_subscriptions.add()
#             subscription.contract_id = contract_id
#             subscription.request_id = self.msg_id # Everytime this is called, it increase by 1
#             subscription.level = level
# =============================================================================
            # Send message
            self._conn._client.send_client_message(client_msg)
            #print("----------------------------")
            #print(f"contract_id={contract_id}, Attempt: {attempt}, send_request with ID {contract_id}")
            #print('request_real_time')
            i = 0
            #while True:
            while i < self.total_recv_cycle:
                #print(f"Trial {i}: msg_id: {subscription.request_id}")
                server_msg = self._conn._client.receive_server_message()
                #print(server_msg)
                i+=1
                # 1) Condition for having receieved a real_time_market_data
                cond_existence = (len(server_msg.real_time_market_data) > 0) 
                
                if cond_existence: #Check for existence of real_market_data
                    # 2) Condition for having the right ID
                    cond_ID = (server_msg.real_time_market_data[0].contract_id == contract_id) 
                    # 3) Condition for having the quote data
                    cond_quote = (len(server_msg.real_time_market_data[0].quotes)>0) 
                    #print("Conditions Check:")
                    #print("(msg recv, Correct ID, Quote recv):", 
                    #      cond_existence, cond_ID, cond_quote, 
                    #      'ID recv:', server_msg.real_time_market_data[0].contract_id)

                    if cond_ID and cond_quote: # check for validity of quote
                        timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                        price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                        volume = server_msg.real_time_market_data[0].quotes[0].volume.significand
                        
                        #self.datafeed_pool[symbol].tick_buffer.add_tick(price, 
                        #                                                volume, 
                        #                                                timestamp)
                        #self.datafeed_pool[symbol].tick_buffer_stat()
                        #print(timestamp, price, volume) 
                        return timestamp, price, volume
                    
                # Delay x seconds for each receive message attempt
                await asyncio.sleep(self.recv_cycle_delay)

            # Delay x seconds for each send message attempt
            await asyncio.sleep(self.send_cycle_delay)
        # return Default values if no correct quote message was caught
        return default
    
    async def reset_tracker(self, contract_id: int) -> None:
        # A function to cancel subscription for the real-time data
        client_msg = build_reset_tracker_request_msg(self.msg_id, contract_id)
# =============================================================================
#         client_msg = ClientMsg()
#         subscription = client_msg.market_data_subscriptions.add()
#         subscription.contract_id = contract_id
#         subscription.request_id = self.msg_id
#         subscription.level = 0
# =============================================================================
        self._conn._client.send_client_message(client_msg)
        i = 0
        #while True:
        while i < self.total_recv_cycle:
            #print(f"Trial {i}: msg_id: {subscription.request_id}")
            server_msg = self._conn._client.receive_server_message()
            i+=1
            
            if len(server_msg.market_data_subscription_statuses)>0:
                status = server_msg.market_data_subscription_statuses[0].status_code
                recv_contract_id = server_msg.market_data_subscription_statuses[0].contract_id
                # Return nothing when we recieve the correct ID with status code
                # success
                if recv_contract_id == contract_id and status == 0:
                    return 
    
    async def run(self, sym: str, contract_ids: dict[str, int]) -> tuple[int|float]:
        
        #for sym in self.symbols:
        # Request real-time data
        output = await self.request_realtime_data(contract_ids[sym])
                                                       
        await self.reset_tracker(contract_ids[sym]) # Reset tracker
        # get the data from  other symbols
        return output

    