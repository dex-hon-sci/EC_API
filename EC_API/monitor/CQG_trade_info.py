#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:13:43 2025

@author: dexter
"""
import datetime
from WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg

from EC_API.connect.base import ConnectCQG
from EC_API.monitor.base import Monitor
# MonitorActiveOrder/ MonitorActivePosition
class MonitorTrade_CQG(Monitor):
    def __init__(self, 
                 connection: ConnectCQG, 
                 account_id: int):
        self._connection = connection
        self._connection.logon()
        self.account_id = account_id

        return
    
    async def request_historical_orders(self,
                                        from_date: datetime.datetime, 
                                        to_date: datetime.datetime) -> ServerMsg:
        
        from_date_timestamp = from_date.timestamp()
        to_date_timestamp = to_date.timestamp()
        
        client_msg = ClientMsg()
    
        information_request = client_msg.information_requests.add()
        
        information_request.id = self.msg_id
        information_request.historical_orders_request.from_date = int(from_date_timestamp)
        information_request.historical_orders_request.to_date = int(to_date_timestamp)
        information_request.historical_orders_request.account_ids.append(self.account_id)
            
        self._connection._client.send_client_message(client_msg)
        while True:
            server_msg = self._connection._client.receive_server_message()
    
            if server_msg.information_reports[0].historical_orders_report is not None:
                return information_request, server_msg
    
    def reset_tracker() -> ServerMsg:
        
        return
    
    def run():
        return 