#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 13:55:48 2025

@author: dexter
"""
import datetime
import time

def generate_time_inverval(datetime: datetime.datetime, 
                           epi: float):
    # generate a tuple of time interval given 
    # epi is in seconds
    start_time = time
    end_time = datetime + datetime.datetime.timedelta(seconds=epi)
    return (start_time, end_time)

today = datetime.datetime.today()
today_date = today.date()
today_str = today.strftime("%Y-%m-%d")

print(datetime.datetime.now())

TIME1 = "09:30:00"
TIME1_dt = datetime.datetime.strptime(today_str+" "+TIME1, 
                                      "%Y-%m-%d %H:%M:%S")
TIME1_dt_interval = generate_time_inverval(TIME1_dt, 2)

TIME2 = "15:45:00"

# generate time interval

ORDER_TIMES = [TIME1, TIME2]
    
while True:
    # define refresh rate and time
    now = datetime.datetime.now()
    time.sleep(4)
    current_time_str = now.strftime("%H:%M")
    # ==============================================
    # Layer 0: check time, payload conditions, 
    # move Payload from Storage to Chamber.
    # ==============================================

    
    # ==============================================
    # Layer 1: check time, payload conditions, 
    # move Payload from Storage to Chamber.
    # ==============================================
    # Runthrough the Order list to see if the current market condition
    # matches the conditions of the orders
    # Time is feature0 
    # price is feature1
    
    for t in ORDER_TIMES:
        pass
        # Send order only if it hasn’t been sent yet today
        #if current_time_str == t and sent_orders.get(t) != now.date():
        #    await place_order(client, t)
        #    sent_orders[t] = now.date()

    # ==============================================
    # Layer 2: Read Payload Chamber, translate
    # Payload to Orders, Send ORders, Change Payload
    # Status.
    # ==============================================

    # ==============================================
    # Layer 3: Check Order Status, Check position 
    # Status, Check account Summary.
    # ==============================================

