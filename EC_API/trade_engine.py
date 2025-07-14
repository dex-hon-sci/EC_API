#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 06:56:14 2025

@author: dexter

A module that control the trade decision and execution through CQG Web API
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
from ordering import LiveOrder
from payload import Payload

import datetime
# Trade engine is incharge of scanning the operational database and
# figure out the time to send the orders

class TradeEngine():
    #Trade eingine manage connection and status of the orders a
    def __init__(self, connection: ConnectCQG):
        self._connection = connection
        self._connection.logon()

    def connection(self):
        return self._connection
        
    async def run():
        while True:
            # Clock ticking
            # Very important metrics
            dt = datetime.datetime.now()
            
            # Scan Chamber DB, load the entries in memory
            # try Sending Order via ordering
            # Check if the order is received 
            # If Yes, move payload from chamber to shellpile 
            # (Copy to shellpile )
            
            # Check the status of the old filled orders
            # change the status in Chamber to filled ShellPile

            if dt > 0 and dt < 1:
                # await send_order()
                pass
            
        
        
        return 
    
    
    #def intake(payload:Payload):
    #    return 

# =============================================================================
#     def goflat():
#         LP = LiveOrder(self._connection, )
#         # A function to initialise the state of the account
# 
#         WHEN_UTC_TIMESTAMP = datetime.datetime.now(timezone.utc) #+ datetime.timedelta(seconds=2)
#         print('WHEN_UTC_TIMESTAMP', WHEN_UTC_TIMESTAMP)
#         #logger.info(f'WHEN_UTC_TIMESTAMP = {WHEN_UTC_TIMESTAMP}')
#         
#         goflat_order_request(client, int(random_string(length=7)), account_id, 
#                              when_utc_timestamp = WHEN_UTC_TIMESTAMP)
#         #logger.info('Send GoFlat Request')
#         logoff_obj, logoff_server_msg = self._connection.logoff(client)
#         #logger.info('Logoff')
# 
#         client.disconnect()
# =============================================================================
