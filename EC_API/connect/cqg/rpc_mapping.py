#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 19 15:54:46 2025

@author: dexter
"""

from EC_API.connect.enums import ConnectionState
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult as LOR
from EC_API.ext.WebAPI.user_session_2_pb2 import LoggedOff as LOff
from EC_API.ext.WebAPI.user_session_2_pb2 import RestoreOrJoinSessionResult as Restore


REQUEST_TO_REPLY = {
  "logon": "logon_result",
  "logoff": "logged_off",
  "restore_or_join_session": "restore_or_join_session_result",
  "ping": "pong",
  "pong": "ping",
  #
  "information_requests": "information_reports",
  #
  "trade_subscriptions": "trade_subscription_statuses",
  #
  "order_requests":"order_statuses",
  #
  "market_data_subscriptions": "market_data_subscription_statuses",
  #
  "time_and_sales_requests": "historical_data_reports",
  "time_bar_requests": "time_and_sales_reports",
  "volume_profile_requests": "",
#
  
  "historical_orders_request": "historical_orders_report"
}