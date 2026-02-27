#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 18:00:18 2026

@author: dexter
"""
from EC_API.connect.cqg.base import ConnectCQG
from tests.unit.fixtures.proxy_clients import FakeCQGClient

def setup():
    host_name = ""
    user_name = "" 
    password = ""
    FkClient = FakeCQGClient()
    conn = ConnectCQG(host_name, user_name, password,client=FkClient)
    
    conn._msg_router
    conn.market_data_stream
    conn.exec_stream
    

def msg_stream():
    ...

def test_router_loop():
    ...