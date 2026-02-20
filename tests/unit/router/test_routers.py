#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:56:37 2026

@author: dexter
"""
from EC_AportPI.connect.cqg.base import ConnectCQG

async def test_non_blocking_ops():
    host_name = ""
    user_name = ""
    password = ""
    connect = ConnectCQG(host_name, user_name, password)
    
    