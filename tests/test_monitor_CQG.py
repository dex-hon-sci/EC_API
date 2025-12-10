#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:41:38 2025

@author: dexter
"""
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
# Python Package imports
import numpy as np
# EC_API imports
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.cqg.realtime_data import MonitorRealTimeDataCQG

load_dotenv() # Loads variables from .env
CQG_host_url = os.getenv("CQG_API_host_name_live")
CQG_live_data_acc = os.getenv("CQG_API_data_live_usrname")
CQG_live_data_pw = os.getenv("CQG_API_data_live_pw")
CQG_live_data_privatelabel = os.getenv("CQG_API_data_live_private_label")
CQG_live_data_client_app_id = os.getenv("CQG_API_data_live_client_app_id")


# =============================================================================
# host_name = 'wss://demoapi.cqg.com:443'
# #user_name = 'EulerWAPI'
# #password = 'WAPI'
# user_name = 'EulerWMD'
# password = 'Li@96558356'#'WMD'
# =============================================================================


SYMS = ["CLE", "HOE", "RBE"]

CC = ConnectCQG(CQG_host_url, CQG_live_data_acc, CQG_live_data_pw)
CC.logon(client_app_id=CQG_live_data_client_app_id,
         private_label=CQG_live_data_privatelabel)
Mon = MonitorRealTimeDataCQG(CC)

CONTRACT_IDS = dict()
CONTRACT_METADATA = dict()


async def resolve():
    msg_id = 0
    for sym in SYMS:
       await Mon.resolve_symbol(sym, msg_id, CONTRACT_IDS, CONTRACT_METADATA)
       msg_id+=1
       
async def pull_data():
    i=0
    while i < 100:
        for sym in SYMS:
            tup = await Mon.run(sym, CONTRACT_IDS)
            print(f"{i},{sym}:", tup)
        i += 1
       
asyncio.run(resolve())
#print(CONTRACT_IDS, CONTRACT_METADATA)
asyncio.run(pull_data())

CC.disconnect()
    
    

