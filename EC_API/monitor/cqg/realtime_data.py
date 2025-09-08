#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:06:40 2025

@author: dexter
"""
import asyncio
# Import EC_API scripts
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.base import Monitor
from EC_API.monitor.tick import TickBuffer
from EC_API.monitor.tick_stats import TickBufferStat
from EC_API.monitor.data_feed import DataFeed

class MonitorRealTimeDataCQG(Monitor):
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        #self._connection.logon()
        self._msg_id: int = 200 # just a starting number for message id
        self.symbols: list = [str]
        self.data_buffers: dict[str, TickBuffer] = {}
        
        self._contract_ids = {
            f'{sym}': self._connection.resolve_symbol(sym, 1).contract_id 
                             for sym in self.symbols
            }
        self._contract_metadata = {
            f'{sym}': self._connection.resolve_symbol(sym, 1)
                                   for sym in self.symbols
            }     
        
        self.total_recv_cycle: int = 20
        self.total_send_cycle: int = 2
        self.recv_cycle_delay: int = 0
        self.send_cycle_delay: int = 0

    def connection(self):
        return self._connection
    
    def _resolve_symbol():
        return 
    
    async def request_real_time(self, 
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
            client_msg = ClientMsg()
            subscription = client_msg.market_data_subscriptions.add()
            subscription.contract_id = contract_id
            subscription.request_id = self.msg_id
            subscription.level = level
            # Send message
            self._connection._client.send_client_message(client_msg)
            print("----------------------------")
            print(f"contract_id={contract_id}, Attempt: {attempt}, send_request with ID {contract_id}")
            #print('request_real_time')
            i = 0
            #while True:
            while i < self.total_recv_cycle:
                print(f"Trial {i}: msg_id: {subscription.request_id}")
                server_msg = self._connection._client.receive_server_message()
                #print(server_msg)
                i+=1
                # 1) Condition for having receieved a real_time_market_data
                cond_existence = (len(server_msg.real_time_market_data) > 0) 
                
                if cond_existence: #Check for existence of real_market_data
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
                        
                        T = Tick(price, volume, timestamp)
                        #print(timestamp, price, volume) 
                        return timestamp, price, volume
                    
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
        client_msg = ClientMsg()
        subscription = client_msg.market_data_subscriptions.add()
        subscription.contract_id = contract_id
        subscription.request_id = self.msg_id
        subscription.level = 0
        self._connection._client.send_client_message(client_msg)
        i = 0
        #while True:
        while i < self.total_recv_cycle:
            #print(f"Trial {i}: msg_id: {subscription.request_id}")
            server_msg = self._connection._client.receive_server_message()
            i+=1
            
            if len(server_msg.market_data_subscription_statuses)>0:
                status = server_msg.market_data_subscription_statuses[0].status_code
                recv_contract_id = server_msg.market_data_subscription_statuses[0].contract_id
                # Return nothing when we recieve the correct ID with status code
                # success
                if recv_contract_id == contract_id and status == 0:
                    return 
    
    async def run(self) -> dict[str|int|float]:
        # Get contract_id from resolve symbol
        
        self.request_real_time() # Request real-time data
        
        await self.reset_tracker() # Reset tracker
        # get the data from  other symbols