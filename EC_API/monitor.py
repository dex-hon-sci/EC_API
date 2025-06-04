#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 18:39:16 2025

@author: dexter
"""
import time
import datetime
from datetime import timezone

from WebAPI.webapi_2_pb2 import ClientMsg

# Import EC_API scripts
from EC_API.connect import ConnectCQG


class Monitor(object):
    # One logon, continuous 
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        self._connection.logon()

        self._time_bucket = []
        self._price_bucket = []
        self._vol_bucket = []
        
        self._msg_id = 200
    def connection(self):
        return self._connection
    
    @property
    def msg_id(self):
        # msg_id updates every time it is called. 
        # This ID is shared by the entire Monitor object.

        self._msg_id += 1
        return self._msg_id 
    
    def request_real_time(self, contract_id:int, msg_id:int, level:int=1, 
                          total_recv_cycle:int = 5, total_send_cycle: int =3,
                          recv_cycle_delay: int =0, send_cycle_delay: int = 1,
                          default_timestamp: float | int = 9, 
                          default_price: float | int = 9, 
                          default_volume: float | int =9):
        
        for attempt in range(total_send_cycle):
            client_msg = ClientMsg()
            subscription = client_msg.market_data_subscriptions.add()
            subscription.contract_id = contract_id
            subscription.request_id = self.msg_id
            subscription.level = level

            self._connection._client.send_client_message(client_msg)
            print(f" Attempt: {attempt}")
            #print('request_real_time')
            i = 0
            #while True:
            while i < total_recv_cycle:
                print(f"Trial {i}: ha")
                server_msg = self._connection._client.receive_server_message()
                print(server_msg)
                i+=1
                # 1) Condition for having receieved a real_time_market_data
                cond_existence = (len(server_msg.real_time_market_data) > 0) 
                
                if cond_existence: #Check for existence of real_market_data
                    # 2) Condition for having the right ID
                    cond_ID = (server_msg.real_time_market_data[0].contract_id == contract_id) 
                    # 3) Condition for having the quote data
                    cond_quote = (len(server_msg.real_time_market_data[0].quotes)>0) 
                    print(cond_existence, cond_ID, cond_quote)
    
                    if cond_ID and cond_quote: # check for validity of quote
                        timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                        price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                        volume = server_msg.real_time_market_data[0].quotes[0].volume.significand
                    
                        return timestamp, price, volume
                    
                # Delay x seconds for each receive message attempt
                time.sleep(recv_cycle_delay)

            # Delay x seconds for each send message attempt
            time.sleep(send_cycle_delay)
        # return Default values if no correct quote message was caught
        return default_timestamp, default_price, default_volume

        
    def track_real_time_inst(self, contract_id: int, msg_id: int, 
                             initial_dt=9, initial_price=9, initial_volume=9,
                             level = 1):
        #dt, price, volume = self.request_real_time(contract_id, msg_id, level)
        #dt0, price0, volume0 = dt, price, volume

        try:
            dt, price, volume = self.request_real_time(contract_id, msg_id, level)
            dt0, price0, volume0 = dt, price, volume
        except:
           print('Exception')
           dt0, price0, volume0 = initial_dt, initial_price, initial_volume
           pass
        print(dt0, price0)
        return dt0, price0, volume0

if __name__ == "__main__":
    host_name = 'wss://demoapi.cqg.com:443'
    user_name = 'EulerWMD'
    password = 'Li@96558356'
    resolveSymbolName = 'QO'

    C = ConnectCQG(host_name, user_name, password)
    M = Monitor(C)
    contract_id = M._connection.resolve_symbol(resolveSymbolName, 1).contract_id

    i = 0
    while True:
        M.track_real_time_inst(contract_id,1)
        i +=1
