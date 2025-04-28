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

def selector():
    return 

class Monitor(object):
    # One logon, continuous 
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        self._connection.logon()

        self._time_bucket = []
        self._price_bucket = []
        self._vol_bucket = []
        
    def connection(self):
        return self._connection
    
    
    def request_real_time(self, contract_id, msg_id, level):
        client_msg = ClientMsg()
        subscription = client_msg.market_data_subscriptions.add()
        subscription.contract_id = contract_id
        subscription.request_id = msg_id
        subscription.level = level
        self._connection._client.send_client_message(client_msg)
        
        while True:
            server_msg = self._connection._client.receive_server_message()

            if len(server_msg.real_time_market_data) > 0 and \
               len(server_msg.real_time_market_data[0].quotes)>0:
                timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                #dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)
                price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                volume = 100

                #volume = server_msg.real_time_market_data[0].quotes[0].volume[0].significand
                #break
                print(timestamp, price, volume)
        #return server_msg
                return timestamp, price, volume

    def track_real_time(self, symbol_name: str):
        self._connection.logon()
        msg_id = 1
        contract_id = self._connection.resolve_symbol(symbol_name, msg_id).contract_id
        msg_id += 1

        #self.request_real_time(contract_id, msg_id, 2)
        
        # This sample doesn't have multiple threads, it subscribe for 5 seconds and unsubscribe
        t_end = time.time() + 30
        #while True:
        i = 0
        #while time.time() < t_end:
        while True:
            msg_id+=1
            print('msg_id', msg_id)
            msg = self.request_real_time(contract_id, msg_id, 1)
            #print('msg', msg)

            if len(msg.real_time_market_data) > 0:
                timestamp = msg.real_time_market_data[0].quotes[0].quote_utc_time
                dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)

                self._price_bucket.append(msg.real_time_market_data[0].quotes[0].scaled_price)
                self._time_bucket.append(dt)
                self._vol_bucket.append(msg.real_time_market_data[0].quotes[0].volume.significand)
                #print("price_bucket", self._price_bucket)
                #print("time_bucket", self._time_bucket)
                #print("vol_bucket", self._vol_bucket)
                
                #self._price_bucket.append(msg.real_time_market_data[0].market_values[0].scaled_last_trade_price)
                #self._time_bucket.append(msg.real_time_market_data[0].market_values[0].last_trade_utc_timestamp.seconds)
                #self._vol_bucket.append(msg.real_time_market_data[0].market_values[0].tick_volume)
                #print(len(msg.real_time_market_data[0].quotes),
                #      type(msg.real_time_market_data[0].quotes))
                time.sleep(5)
            
                i+=1
            #if i >5:
            #    break
        
    def track_real_time_inst(self, contract_id, msg_id, 
                             initial_dt=9, initial_price=9, initial_volume=9):
        # Send request to query real-rime data . Best used in a while loop.
        try:
            dt, price, volume = self.request_real_time(contract_id, msg_id, 1)
            dt0, price0, volume0 = dt, price, volume
        except:
            print('Exception')
            dt0, price0, volume0 = initial_dt, initial_price, initial_volume
            pass
        print('price', dt0, price0, volume0)
        return dt0, price0, volume0

if __name__ == "__main__":
    import load_dotenv
    import os
    load_dotenv()
    host_name = os.environ.get("CQG_API_host_name_demo")
    user_name = os.environ.get("CQG_API_data_demo_usrname")
    password = os.environ.get("CQG_API_data_demo_pw")

    print(host_name, user_name, password)
    resolveSymbolName = 'QOM25'  #'F.US.ZUI'

# =============================================================================
#     C = ConnectCQG(host_name, user_name, password)
#     M = Monitor(C)
#     contract_id = M._connection.resolve_symbol(resolveSymbolName, 1).contract_id
# 
#     i = 0
#     while True:
#         time.sleep(2)
#         M.track_real_time_inst(contract_id,1)
#         i +=1
#     
# =============================================================================
