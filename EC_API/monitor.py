#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 18:39:16 2025

@author: dexter
"""
import time
import datetime
from datetime import timezone

from dotenv import load_dotenv
import os
load_dotenv()

from WebAPI.webapi_2_pb2 import ClientMsg
import numpy as np
# Import EC_API scripts
#from EC_API.connect import ConnectCQG
from connect import ConnectCQG

class Monitor(object):
    # One logon, continuous 
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        self._connection.logon()

    def connection(self):
        return self._connection
    
    def request_real_time(self, 
                          contract_id: int, msg_id: int, level: int,
                          default_timestamp: int = 404, 
                          default_price: int = 404, 
                          default_volume: int = 404):
        # request real-time data for a single contract
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
                volume = server_msg.real_time_market_data[0].quotes[0].volume
                return timestamp, price, volume
            
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
        return dt0, price0, volume0
    
    def request_real_time_multi(self, 
                                syms: list[str], contract_ids: list[int], 
                                msg_ids: list[int], levels: list[int], 
                                total_attempt_number: int = 3,
                                initial_dict: dict[str| float] = dict()):
        """
        A function that take a list of symbols and corresponding contract ids, 
        and then send it through websocket to retrieve real-time data. 
        This is a sub-optimal solution due to CQG not allowing concurrent 
        sessions. 
        
        All real-time retrieval are tied together in this function.

        Parameters
        ----------
        syms : list
            A list of symbols.
        contract_ids : list
            DESCRIPTION.
        msg_ids : list
            DESCRIPTION.
        levels : list
            DESCRIPTION.
        total_attempt_number : int, optional
            DESCRIPTION. The default is 3.
        initial_dict : dict, optional
            DESCRIPTION. The default is dict().

        Returns
        -------
        msg_dict : TYPE
            Message Dictionary contains.

        """
        
        # Take in an initial_dict for default output.
        # In the case of receiving no valid message, the default dict component
        # is return
        msg_dict = initial_dict
        # request real-time data for multiple contracts
        #client_msg = ClientMsg()
        
        for sym, contract_id, msg_id, level in zip(syms, contract_ids, 
                                                   msg_ids, levels):
            client_msg = ClientMsg()

            subscription = client_msg.market_data_subscriptions.add()

            subscription.contract_id = contract_id
            subscription.request_id = msg_id
            subscription.level = level
            
            print('sym', sym, contract_id, msg_id, level)
            
            self._connection._client.send_client_message(client_msg)
            
            attempt_number = 0
            while attempt_number <= total_attempt_number: # recommend do not exceed 10
                server_msg = self._connection._client.receive_server_message()
                print(attempt_number)
                # Only when the recieved msg contains quotes do we record 
                # the real-time data
                if len(server_msg.real_time_market_data) > 0 and \
                   len(server_msg.real_time_market_data[0].quotes)>0 and\
                   server_msg.real_time_market_data[0].contract_id == contract_id:
                   
                   timestamp = server_msg.real_time_market_data[0].quotes[0].quote_utc_time
                   price = server_msg.real_time_market_data[0].quotes[0].scaled_price
                   volume = server_msg.real_time_market_data[0].quotes[0].volume
                   
                   # update only the symbol with new data
                   msg_dict[sym] = (timestamp, price, volume)
                   break
                else:
                   attempt_number +=1
                  
                           
        return msg_dict
    
    def track_real_time_inst_multi(contract_ids, msg_ids):
        
        return 
# =============================================================================
#     def track_real_time(self, symbol_name: str):
#         self._connection.logon()
#         msg_id = 1
#         contract_id = self._connection.resolve_symbol(symbol_name, msg_id).contract_id
#         msg_id += 1
# 
#         #self.request_real_time(contract_id, msg_id, 2)
#         
#         # This sample doesn't have multiple threads, it subscribe for 5 seconds and unsubscribe
#         t_end = time.time() + 30
#         #while True:
#         i = 0
#         #while time.time() < t_end:
#         while True:
#             msg_id+=1
#             print('msg_id', msg_id)
#             msg = self.request_real_time(contract_id, msg_id, 1)
#             #print('msg', msg)
# 
#             if len(msg.real_time_market_data) > 0:
#                 timestamp = msg.real_time_market_data[0].quotes[0].quote_utc_time
#                 dt = datetime.datetime.fromtimestamp(timestamp, tz=timezone.utc)
# 
#                 self._price_bucket.append(msg.real_time_market_data[0].quotes[0].scaled_price)
#                 self._time_bucket.append(dt)
#                 self._vol_bucket.append(msg.real_time_market_data[0].quotes[0].volume.significand)
#                 #print("price_bucket", self._price_bucket)
#                 #print("time_bucket", self._time_bucket)
#                 #print("vol_bucket", self._vol_bucket)
#                 
#                 #self._price_bucket.append(msg.real_time_market_data[0].market_values[0].scaled_last_trade_price)
#                 #self._time_bucket.append(msg.real_time_market_data[0].market_values[0].last_trade_utc_timestamp.seconds)
#                 #self._vol_bucket.append(msg.real_time_market_data[0].market_values[0].tick_volume)
#                 #print(len(msg.real_time_market_data[0].quotes),
#                 #      type(msg.real_time_market_data[0].quotes))
#                 time.sleep(5)
#             
#                 i+=1
#             #if i >5:
#             #    break
# =============================================================================
        


if __name__ == "__main__":
    host_name = os.environ.get("CQG_API_host_name_demo")
    user_name = os.environ.get("CQG_API_data_demo_usrname")
    password = os.environ.get("CQG_API_data_demo_pw")

    print(host_name, user_name, password)
    resolveSymbolName = 'QOM25'  #'F.US.ZUI'
    
    sym_list = ['F.US.ZUC', 'QON25', 'QOM25', 'QPM25', 'QPN25']
    ids = np.array([13123,5511,103,434,666]) 
    levels = [1,1,1,1,1]

    C = ConnectCQG(host_name, user_name, password)
    M = Monitor(C)
    contract_ids = []
    for i, sym in zip(ids, sym_list):
        contract_ids.append(M._connection.resolve_symbol(sym, i).contract_id)
    
    print('contract_ids', contract_ids)
    #.request_real_time_multi(contract_ids, ids, levels)
    Initial_dict = M.request_real_time_multi(sym_list, contract_ids, ids, levels)
    print(Initial_dict)
    # This sample doesn't have multiple threads, it subscribe for 5 seconds and unsubscribe
    t_end = time.time() + 10
    
    while True:
        print('-----------------------')
        print(datetime.datetime.now())
        ids = ids + 1 #[ele +1 for ele in ids]
        msg_dict = M.request_real_time_multi(sym_list, contract_ids, ids, levels,
                                             total_attempt_number= 3,
                                             initial_dict=Initial_dict)
        Initial_dict = msg_dict
        print('msg_dict', msg_dict)
        time.sleep(1)
        #request_real_time(client, contract_id, msg_id, 7)
        
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
