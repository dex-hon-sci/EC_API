#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:41:38 2025

@author: dexter
"""
from datetime import datetime, timedelta
import asyncio
# Python Package imports
import numpy as np
# EC_API imports
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.monitor.cqg.realtime_data import MonitorRealTimeDataCQG

HOST_NAME = 'wss://demoapi.cqg.com:443'
USRNAME = 'EulerWMD'
PW = 'Li@96558356'

# =============================================================================
# host_name = 'wss://demoapi.cqg.com:443'
# #user_name = 'EulerWAPI'
# #password = 'WAPI'
# user_name = 'EulerWMD'
# password = 'Li@96558356'#'WMD'
# =============================================================================


SYMS = ["CLE", "HOE", "RBE"]

CC = ConnectCQG(HOST_NAME, USRNAME, PW)
CC.logon()
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
    
    

