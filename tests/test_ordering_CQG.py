#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 10:41:19 2025

@author: dexter
"""
import time
import datetime
import logging
from datetime import timezone
import pytest        

#from WebAPI.webapi_2_pb2 import *
from EC_API.ext.WebAPI import webapi_client
from EC_API.ext.WebAPI.user_session_2_pb2 import LogonResult
from EC_API.ext.WebAPI.metadata_2_pb2 import ContractMetadata, SymbolResolutionReport
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus, PositionStatus
from EC_API.connect.base import ConnectCQG
from EC_API.utility.base import random_string
from EC_API.ordering.CQG_LiveOrder import CQGLiveOrder
from EC_API.ordering.enums import SUBSCRIPTION_SCOPE_ORDERS, RequestType
from EC_API.ordering.enums import *
from tests.ordering_cases import (
    NewOrderCases, 
    ModifyOrderCases, 
    CancelOrderCases,
    ActivateOrderCases
    )

HOST_NAME = 'wss://demoapi.cqg.com:443'
USR_NAME = ''
PASSWORD = ''
ACCOUNT_ID = 00000

# Define logger object
logger = logging.getLogger(__name__)
# =============================================================================
# logging.basicConfig(filename='./log/test_run_order.log', 
#                     level=logging.INFO,
#                     format="%(asctime) s%(levelname)s %(message)s",
#                     datefmt="%Y-%m-%d %H:%M:%S")
# =============================================================================
logging.basicConfig(filename='./log/temp.log', 
                    level=logging.INFO,
                    format="%(asctime) s%(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


symbols = ["",""]
LMT_price = [0,0]
STP_price = [0,0]

@pytest.mark.parametrize() 
def test_success_order_requests(symbol_name: str,
                                scaled_limit_price: int, 
                                scaled_stop_price: int) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    #logger.info('========(Start test_success_order_requests)========')
    # 1.Send Logon message with valid credentials.
    #logger.info('1.Send Logon message with valid credentials.')
    NOC = NewOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    NOC.run_all(scaled_limit_price, scaled_stop_price)
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()
    
@pytest.mark.parametrize() 
def test_modify_order(symbol_name: str,
                      old_LMT_price: int, old_STP_price: int,
                      new_LMT_price: int, new_STP_price: int, 
                      old_qty: int, new_qty: int) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    MOC = ModifyOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    MOC.run_all(old_LMT_price, old_STP_price, 
                new_LMT_price, new_STP_price, 
                old_qty, new_qty)
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()

    
@pytest.mark.parametrize() 
def test_cancel_order(symbol_name: str, 
                      scaled_limit_price: int) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    COC = CancelOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    COC.run_all(scaled_limit_price)
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()
   
@pytest.mark.parametrize() 
def test_activate_order(symbol_name: str):
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    AOC = ActivateOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    AOC.run_all()
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()

@pytest.mark.parametrize() 
def test_success_pos_status_requests(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)

    request_details = {
        "symbol_name": symbol_name,
        "cl_order_id": random_string(length=10),
        "order_type": ORDER_TYPE_MKT,
        "duration": DURATION_DAY, 
        "side": SIDE_BUY,
        "qty_significant": 1, # make sure qty are in Decimal (int) not float
        "qty_exponent": 0, 
        "is_manual": False,
        }

    CLOrder = CQGLiveOrder(CONNECT, 
                           symbol_name = request_details['symbol_name'], 
                           request_id = int(random_string(length=10)), 
                           account_id = ACCOUNT_ID,
                           sub_scope = SUBSCRIPTION_SCOPE_POSITIONS)
    server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                              request_details = request_details)

    assert type(server_msg) == PositionStatus
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()

@pytest.mark.parametrize() 
def test_success_collateral_status_requests(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)

    request_details = {
        "symbol_name": symbol_name,
        "cl_order_id": random_string(length=10),
        "order_type": ORDER_TYPE_MKT,
        "duration": DURATION_DAY, 
        "side": SIDE_BUY,
        "qty_significant": 1, # make sure qty are in Decimal (int) not float
        "qty_exponent": 0, 
        "is_manual": False,
        }

    CLOrder = CQGLiveOrder(CONNECT, 
                           symbol_name = request_details['symbol_name'], 
                           request_id = int(random_string(length=10)), 
                           account_id = ACCOUNT_ID,
                           sub_scope = SUBSCRIPTION_SCOPE_COLLATERAL)
    server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                              request_details = request_details)

    assert type(server_msg) == CollateralStatus
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()


def test_account_summary_status_requests(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    request_details = {
        "symbol_name": symbol_name,
        "cl_order_id": random_string(length=10),
        "order_type": ORDER_TYPE_MKT,
        "duration": DURATION_DAY, 
        "side": SIDE_BUY,
        "qty_significant": 1, # make sure qty are in Decimal (int) not float
        "qty_exponent": 0, 
        "is_manual": False,
        }
    
    CLOrder = CQGLiveOrder(CONNECT, 
                           symbol_name = request_details['symbol_name'], 
                           request_id = int(random_string(length=10)), 
                           account_id = ACCOUNT_ID,
                           sub_scope = SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY)
    server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                              request_details = request_details)

    assert type(server_msg) == AccountSummaryStatus
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()

#test_goflat_request
#test_cancellall_
#test_liquidate_all_

# =============================================================================
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
# =============================================================================

