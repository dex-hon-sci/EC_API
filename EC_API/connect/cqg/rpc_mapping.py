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
  "symbol_resolution": "information_reports",
  "trade_subscribe": "trade_subscription_statuses",
  "md_subscribe": "market_data_subscription_statuses",
  "bar_request": "historical_data_reports",
  "tas_request": "time_and_sales_reports",
  "order_request": "order_statuses",
  "historical_orders": "order_statuses",  # or "order_snapshot"/whatever CQG sends in your case
}