#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  8 10:46:33 2025

@author: dexter
"""
import asyncio
# Import EC_API scripts
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.connect.cqg.base import Connect
from EC_API.monitor.base import Monitor
from EC_API.monitor.tick import TickBuffer, Tick
from EC_API.monitor.tick_stats import TickBufferStat
from EC_API.monitor.data_feed import DataFeed


class MonitorRealTimeData(Monitor):
    """
    MonitorRealTimeData controls what symbols subscriptions are we listening 
    to, how to update TickBuffer and TickBufferStat, and control what is 
    written into the DataFeed object.
    
    DataFeed objects are fed into OpStrategy.
    
    """
    def __init__(self, 
                 connection: Connect,
                 symbols: set):
        self._connection = connection
        #self._connection.logon()
        self._msg_id: int = 200 # just a starting number for message id
        self.symbols: set = symbols
        self.symbol_count: int = len(symbols)
        self.datafeed_pool: dict[str, TickBuffer] = {}
        
        # 
        self.total_recv_cycle: int = 20
        self.total_send_cycle: int = 2
        self.recv_cycle_delay: int = 0
        self.send_cycle_delay: int = 0

    def connection(self):
        return self._connection
    
    async def _resolve_symbol(self) -> None:
        # Set up contract_id and metadata for references
        for symbol in self.symbols:
            if symbol not in self._contract_ids:
                self._contract_ids[symbol] = self._connection.resolve_symbol(symbol, 1).contract_id 
                self._contract_metadata = self._connection.resolve_symbol(symbol, 1)

    async def _build_datafeed(self) -> None:
        # Set up a pool of datafeed before running monitoring functions
        for symbol in self.symbols:
            if symbol not in self.datafeed_pool: 
                #Add new datafeed if there is a new symbol
                DF = DataFeed(tick_buffer = TickBuffer(60), #60 seconds
                              tick_buffer_stat = TickBufferStat(),
                              symbol = symbol)
                self.datafeed_pool[symbol] = DF
        
    
    async def request_real_time(self, 
                                symbol: str,
                                contract_id:int, 
                                level: int = 1, 
                                default_timestamp: float | int = 9, 
                                default_price: float | int = 9, 
                                default_volume: float | int = 9) -> ServerMsg:
        # Two loop approach: Not the most sophisticated but will do for now.
        # Could Use continuous scrapping with a buffer. Send all requests, recv
        # msg, scrap them and bank them in our buffer. Then we post it on the TSDB
        
        # Send request msg and rev response, stop the func when we get the three
        # condition correct: 1) recv real_time_market_data, 2) right ID, 3) recv
        # quote data.
        for attempt in range(self.total_send_cycle):

            # Send message
            print("----------------------------")
            print(f"contract_id={contract_id}, Attempt: {attempt}, send_request with ID {contract_id}")
            #print('request_real_time')
            i = 0
            while i < self.total_recv_cycle:
                server_msg = self._connection._client.receive_server_message()
                #print(server_msg)
                i+=1
                # 1) Condition for having receieved a real_time_market_data
                cond_existence = (len(server_msg.real_time_market_data) > 0) 
                
                # 2) Condition for having the right ID
                cond_ID = (server_msg.real_time_market_data[0].contract_id == contract_id) 
                # 3) Condition for having the quote data
                cond_quote = (len(server_msg.real_time_market_data[0].quotes)>0) 
                print("Conditions Check:")
                print("(msg recv, Correct ID, Quote recv):", 
                      cond_existence, cond_ID, cond_quote, 
                      'ID recv:', server_msg.real_time_market_data[0].contract_id)

                if cond_ID and cond_quote: # check for validity of quote
                    timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                    price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                    volume = server_msg.real_time_market_data[0].quotes[0].volume.significand
                    
                    # Add a Tick to the correct datafeed tick_buffer
                    self.datafeed_pool[symbol].tick_buffer.add_tick(price, 
                                                                    volume, 
                                                                    timestamp)
                    return
                    
                # Delay x seconds for each receive message attempt
                await asyncio.sleep(self.recv_cycle_delay)

            # Delay x seconds for each send message attempt
            await asyncio.sleep(self.send_cycle_delay)
        # return Default values if no correct quote message was caught
        return default_timestamp, default_price, default_volume
    
    async def reset_tracker(self, 
                            contract_id: int, 
                            ) -> ServerMsg:
        # A function to cancel subscription for the real-time data
        pass
    
    async def run(self) -> dict[str|int|float]:
        
        if self.symbol_count < len(self.symbols):  
            try: # If there are more symbols than the 
                await self._resolve_symbol() # Get contract_id from resolve symbol
                await self._build_datafeed() # Setup data feed
                # Add 
                self.symbol_count +=len(self.symbols) - self.symbol_count
            except:
                print("Unable to resolve symbol and build a new DataFeed for\
                      the new symbol.")
                      
        await self.request_real_time() # Request real-time data
        await self.reset_tracker() # Reset tracker
