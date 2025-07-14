#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 17:47:03 2025

@author: dexter

This is the script that continuously load the newest data inflow and 
generate order payload and store them in storage.

It also moves the ready payload to chamber routinely (based on time)

Signal-> Payload
"""
import datetime

async def main_loop():
    while True:
        dt = datetime.datetime.now()
        
        # Check the time of the Storage
        # Move from Storage to Chamber based on time

        
        
    return
