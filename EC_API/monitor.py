#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 18:39:16 2025

@author: dexter
"""
import time
import datetime
from datetime import timezone

from .WebAPI.webapi_2_pb2 import ClientMsg

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
                print(len(server_msg.real_time_market_data), 
                      len(server_msg.real_time_market_data[0].quotes))
                
                timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                #dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)
                price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                volume = server_msg.real_time_market_data[0].quotes[0].volume.significand

                print(timestamp, price, volume)
                break
            
        return timestamp, price, volume
        
    def track_real_time_inst(self, contract_id: int, msg_id: int, 
                             initial_dt=9, initial_price=9, initial_volume=9):

        try:
            dt, price, volume = self.request_real_time(contract_id, msg_id, 1)
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
    
    #print(M._price_bucket)    
    #print(M._time_bucket)    
    #print(M._vol_bucket)