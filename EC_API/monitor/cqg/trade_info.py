#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 10:13:43 2025

@author: dexter
"""
import asyncio
from datetime import datetime
from EC_API.ext.WebAPI.webapi_2_pb2 import ClientMsg, ServerMsg
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.base import Monitor
from EC_API.monitor.cqg.builders import build_trade_info_request_msg

# MonitorActiveOrder/ MonitorActivePosition
class MonitorTradeCQG(Monitor):
    def __init__(self, 
                 connection: ConnectCQG, 
                 account_id: int):
        self._conn = connection
        self._transport = self._conn._transport

        self.account_id = account_id
        
    def _rid(self) -> int:
        return self.conn.msg_id

    async def request_historical_orders(self,
                                  from_date: datetime, 
                                  to_date: datetime) -> ServerMsg:
        
        from_date_timestamp = from_date.timestamp()
        to_date_timestamp = to_date.timestamp()
        
        rid = self._rid
        client_msg = build_trade_info_request_msg( 
            self.account_id, 
            self._rid,
            from_date,
            to_date
            )
                                     
        key = ("", rid)
        fut = self._router.register(key)
        await self._transport.send(client_msg)
        server_msg = await asyncio.wait_for(fut, timeout=self.timeout)
        
        return server_msg
        #client_msg = ClientMsg()
    
        #information_request = client_msg.information_requests.add()
        #information_request.id = self.msg_id
        #information_request.historical_orders_request.from_date = int(from_date_timestamp)
        #information_request.historical_orders_request.to_date = int(to_date_timestamp)
        #information_request.historical_orders_request.account_ids.append(self.account_id)
            
        #self._connection._client.send_client_message(client_msg)
        return
    
    async def reset_tracker() -> ServerMsg:
        
        return


        
        # Get history open position request
        # Turn that into Json format
        # reset tracker
        # Return Json file, to be posted with prometheus and Grafana
    
    # def get_history_orders():
    #     
    #     #client, msg_id, account_id, from_date, to_date
    #     client = webapi_client.WebApiClient()
    #     client.connect(host_name)
    #     client_msg, logon_obj, logon_server_msg = logon(client, user_name, password)
    #     
    #     from_date = datetime.datetime(2025,7,22,0,0,0, tzinfo=timezone.utc) 
    #     to_date = datetime.datetime.now(timezone.utc) #+ datetime.timedelta(seconds=2)
    #     request_historical_orders(client, int(random_string(length=7)),
    #                               account_id, from_date, to_date)
    #     logoff_obj, logoff_server_msg = logoff(client)
    #     #logger.info('Logoff')
    # 
    #     client.disconnect()
    
    #SessionInformationRequest
    #option_maturity_list_request
    #instrument_group_request
    #at_the_money_strike_request
    #contract_metadata_request
    #order_status_request
    #account_risk_parameters_request