#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 16:32:53 2025

@author: dexter
"""
import time
from WebAPI.webapi_2_pb2 import ClientMsg

# Import EC_API scripts
from EC_API.connect import ConnectCQG

# Monitor live-data
# Monitor our own trading routing related info (position, summary)

class Monitor(object):
    # An Object incharge of 
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        self._connection.logon()

        self._time_bucket = []
        self._price_bucket = []
        self._vol_bucket = []
        
        self._msg_id = 200 # just a starting number for message id

    def connection(self):
        return self._connection
    
    @property
    def msg_id(self):
        # msg_id updates every time it is called. 
        # This ID is shared by the entire Monitor object.
        self._msg_id += 1
        return self._msg_id 
    
    def request_real_time(self, contract_id:int, level:int=1, 
                          total_recv_cycle:int = 20, total_send_cycle: int =2,
                          recv_cycle_delay: int =0, send_cycle_delay: int = 0,
                          default_timestamp: float | int = 9, 
                          default_price: float | int = 9, 
                          default_volume: float | int =9):
        # Two loop approach: Not the most sophisticated but will do for now.
        # Could Use continuous scrapping with a buffer. Send all requests, recv
        # msg, scrap them and bank them in our buffer. Then we post it on the TSDB
        
        # Send request msg and rev response, stop the func when we get the three
        # condition correct: 1) recv real_time_market_data, 2) right ID, 3) recv
        # quote data.
        for attempt in range(total_send_cycle):
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
            while i < total_recv_cycle:
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
                    
                        #print(timestamp, price, volume) 
                        return timestamp, price, volume
                    
                # Delay x seconds for each receive message attempt
                time.sleep(recv_cycle_delay)

            # Delay x seconds for each send message attempt
            time.sleep(send_cycle_delay)
        # return Default values if no correct quote message was caught
        return default_timestamp, default_price, default_volume

    def reset_tracker(self, contract_id, total_recv_cycle=5):
        # A function to cancel subscription for the real-time data
        client_msg = ClientMsg()
        subscription = client_msg.market_data_subscriptions.add()
        subscription.contract_id = contract_id
        subscription.request_id = self.msg_id
        subscription.level = 0
        self._connection._client.send_client_message(client_msg)
        i = 0
        #while True:
        while i < total_recv_cycle:
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
            
    
# MonitorActiveOrder/ MonitorActivePosition
class MonitorTrade():
    def __init__():
        return
    
    def request():
        return

# MonitorRealTimedata

class MonitorRealTimedata():
    def __init__():
        return 
    
    def request_real_time():
        return 
    
    def reset_tracker():
        return