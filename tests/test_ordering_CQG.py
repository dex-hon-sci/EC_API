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
from EC_API.ext.WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus
from EC_API.connect.base import ConnectCQG
from EC_API.utility.base import random_string
from EC_API.ordering.enums import SUBSCRIPTION_SCOPE_ORDERS, RequestType
#from EC_API.ordering.enums import *
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

#test_success_pos_status_requests
#test_success_collateral_status_requests
#test_account_summary_status_requests
#test_goflat_request
#test_cancellall_
#test_liquidate_all_

        
def test_success_pos_status_requests() -> None:
    # Successful Position Status Requests

    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_success_pos_status_requests)========')

    # 1.  Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()
    logger.info('1. Send Logon message with valid credentials')

    print('logon_server_msg', logon_server_msg)
    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')
    
    # 3. Send InformationRequest with symbol_resolution_requests for the \
    # symbols symbol=’F.US.ZUI’.
    symbol1 = "F.US.ZUI"
    msg_id = int(random_string(length=5))
    information_request1, server_msg1 = resolve_symbol(client, symbol1, msg_id)
    logger.info(f'-------(3. Start Testing orders with Symbol1: {symbol1})--------')
    print('step 3 successful')
    
    msg_id +=1
    
    # 4.  Receive InformationReport with SymbolResolutionReport with status_code=’SUCCESS’ and contract_metadata for the symbol.
    assert server_msg1.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'4. Information Report for {symbol1} status_code: SUCCESS')

    # Retrieve Contract metadata
    contract_metadata1 = server_msg1.information_reports[0].symbol_resolution_report.contract_metadata
    
    # check if the contract metadata is in the information report
    assert type(contract_metadata1)==ContractMetadata
    logger.info(f'4. Contract_metadata for {symbol1}: {contract_metadata1}')

    # 5.  Send TradeSubscription with subscribe = true and subscription_scope=POSITIONS.
    trade_sub_request1, status_msg1, \
    trade_server_msg1 = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_POSITIONS)    
    print('trade_sub_request',trade_sub_request1)
    print('server_msg', trade_server_msg1)

    print('step 5 successful')
    # 6.  Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’,\
    # CollateralStatus and TradeSnapshotCompletion.
    print('trade_server_msg1', trade_server_msg1)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. request_trade_subscription for {symbol1}: SUCCESS')

    print('step 6 successful')
    # 7.  Send NewOrder for BUY DAY MKT order and wait until it is filled 
    # (in order to get the fills, application must send TradeSubscription with 
    # subscribe = true and subscription_scope=ORDERS. This is optional for current test.).
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    logger.info(f'7. Send new BUY DAY MKT order for {symbol1}')
    server_msg_NO_BUY_MKT_DAY =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_DAY, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        sub_scope=SUBSCRIPTION_SCOPE_POSITIONS)
    print('server_msg_NO_BUY_MKT_DAY', server_msg_NO_BUY_MKT_DAY)
    print("Wait for 2 seconds")

    # 8.  Receive PositionStatus.    
    logger.info(f'8. PositionStatus: {server_msg_NO_BUY_MKT_DAY}')

    # 9.  Send TradeSubscription with subscribe = false.
    trade_sub_request1, status_msg1, trade_server_msg1 = request_trade_subscription(client, 
                                                                       msg_id, 
                                                                       sub_scope=SUBSCRIPTION_SCOPE_POSITIONS,
                                                                       subscribe= False)
    logger.info(f'9. Sent request_trade_subscription for {symbol1}')

    print('trade_sub_request',trade_sub_request1)
    print('trade_server_msg1', trade_server_msg1)

    # 10. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’.
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'10. request_trade_subscription for {symbol1}: SUCCESS')
    logger.info(f'10. {status_msg1}')

    # 11. Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT.logoff()

    CONNECT.disconnect()
    logger.info('========(End test_success_pos_status_requests)========') 
    # 12. Make sure to run this test, while having an option (e.g. C.EP, P.EP), \
    # an equity (S.MSFT) position.

def test_success_collateral_status_requests() -> None:
    # Successful Collateral Status Requests
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_success_collateral_status_requests)========')

    # 1.  Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()

    print('logon_server_msg', logon_server_msg)
    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')
    
    # 3. Send InformationRequest with symbol_resolution_requests for the \
    # symbols symbol=’F.US.ZUI’.
    symbol1 = "F.US.ZUI"
    msg_id = int(random_string(length=5))
    information_request1, server_msg1 = resolve_symbol(client, symbol1, msg_id)
    logger.info(f'-------(3. Start Testing orders with Symbol1: {symbol1})--------')
    print('step 3 successful')
    
    msg_id +=1

    # 4.  Receive InformationReport with SymbolResolutionReport with 
    # status_code=’SUCCESS’ and contract_metadata for the symbol.
    assert server_msg1.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'4. Information Report for {symbol1} status_code: SUCCESS')

    # Retrieve Contract metadata
    contract_metadata1 = server_msg1.information_reports[0].symbol_resolution_report.contract_metadata
    
    # check if the contract metadata is in the information report
    assert type(contract_metadata1)==ContractMetadata
    logger.info(f'4. Contract_metadata for {symbol1}: {contract_metadata1}')
    
    # 5.  Send TradeSubscription with subscribe = true and subscription_scope= COLLATERAL.
    trade_sub_request1, status_msg1, \
    trade_server_msg1 = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_COLLATERAL)

    print('trade_sub_request',trade_sub_request1)
    print('server_msg1', trade_server_msg1)

    print('step 5 successful')
    # 6.  Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’,\
    # CollateralStatus and TradeSnapshotCompletion.
    print('trade_server_msg1', trade_server_msg1.trade_subscription_statuses)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. request_trade_subscription for {symbol1}: SUCCESS')

    print('step 6 successful')
    
    # 7.  Send NewOrder for BUY DAY MKT order and wait until it is filled.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_BUY_MKT_DAY =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_DAY, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        sub_scope = SUBSCRIPTION_SCOPE_COLLATERAL)
    
    print('server_msg_NO_BUY_MKT_DAY', server_msg_NO_BUY_MKT_DAY)
    logger.info("7. Sent NewOrder for BUY DAY MKT order and wait for 5 secs.")
    time.sleep(5)
    # 8.  Receive CollateralStatus.
    print('8. collateral_statuses', server_msg_NO_BUY_MKT_DAY.collateral_statuses)
    logger.info(f"8.  Receive CollateralStatus: {server_msg_NO_BUY_MKT_DAY}")
    
    # 9.  Send TradeSubscription with subscribe = false.
    print("9: Send unsub msg")
    trade_sub_request2, status_msg2, \
    trade_server_msg2 = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_COLLATERAL,
                                                   subscribe= False)
    logger.info(f'9. Sent request_trade_subscription for {symbol1}')

    print('trade_sub_request2',trade_sub_request2)
    print('server_msg2', trade_server_msg2)

    print('step 9 successful')
    #trade_sub_msg = client.receive_server_message()
    # 10. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’.
    assert status_msg2.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info('10. Receive TradeSubscriptionStatus with status_code = "SUCCESS".')

    # 11. Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT.logoff()
    print('logoff_server_msg', logoff_server_msg)
    CONNECT.disconnect()
    logger.info('========(End test_success_collateral_status_requests)========') 

     

def test_account_summary_status_requests():
    # Successful Account Summary Status Requests
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_account_summary_status_requests)========')

    # 1.  Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()

    print('logon_server_msg', logon_server_msg)
    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')
    
    # 3. Send InformationRequest with symbol_resolution_requests for the \
    # symbols symbol=’F.US.ZUI’.
    symbol1 =  "F.US.ZUC"
    msg_id = int(random_string(length=5))
    information_request1, server_msg1 = resolve_symbol(client, symbol1, msg_id)
    logger.info(f'-------(3. Start Testing orders with Symbol1: {symbol1})--------')
    print('step 3 successful')
    msg_id +=1

    # 4.  Receive InformationReport with SymbolResolutionReport with 
    # status_code=’SUCCESS’ and contract_metadata for the symbol.
    assert server_msg1.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'4. Receive Information Report for {symbol1} status_code: SUCCESS')

    # Retrieve Contract metadata
    contract_metadata1 = server_msg1.information_reports[0].symbol_resolution_report.contract_metadata
    # Retrieve Contract metadata
    sym_res_report = server_msg1.information_reports[0].symbol_resolution_report
    
    # check if the SymbolResolutionReport is in the information report
    assert type(sym_res_report) == SymbolResolutionReport
    # check if the contract metadata is in the information report
    assert type(contract_metadata1)==ContractMetadata
    logger.info(f'4. Receive Contract_metadata for {symbol1}: {contract_metadata1}')
    print('step 4 successful')

    # 5. Send TradeSubscription with subscribe = true and 
    # subscription_scope=ACCOUNTSUMMARY, with AccountSummaryParameters..
    trade_sub_request1, status_msg1, \
    trade_server_msg1 = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY)
                                                   #SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY)
    logger.info(f'5. Sent request_trade_subscription for {symbol1}')

    print('trade_sub_request',trade_sub_request1)
    print('status_msg', status_msg1)
    print('server_msg', trade_server_msg1)

    print('step 5 successful')

    # 6. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’, 
    # OrderStatus with any orders according to PublicationType(ACCOUNT, 
    # SALES_SERIES, BROKERAGE and ALL_AUTHORIZED), and TradeSnapshotCompletion.
    
    print('trade_server_msg1', trade_server_msg1)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. Receive TradeSubscriptionStatus for {symbol1}: SUCCESS')
    print('step 6 successful')

    # 7.  Send NewOrder for BUY DAY MKT order and wait until it is filled.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    logger.info(f'7. Send new BUY DAY MKT order for {symbol1}')
    server_msg_NO_BUY_MKT_DAY =  new_order_request(
                                       client, request_id, 
                                       account_id, contract_id, 
                                       cl_order_id, ORDER_TYPE_MKT, 
                                       DURATION_DAY, SIDE_BUY, 
                                       qty_significant, qty_exponent, 
                                       is_manual,
                                       sub_scope = SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY)
    
    print('server_msg_NO_BUY_MKT_DAY', server_msg_NO_BUY_MKT_DAY)
    # 8.  Receive AccountSummaryStatus.
    assert server_msg_NO_BUY_MKT_DAY.account_summary_statuses is not None
    logger.info(f'8. Account Summary Statuses: {server_msg_NO_BUY_MKT_DAY.account_summary_statuses}')

    # 9.  Send TradeSubscription with subscribe = false.
    trade_sub_request_off, status_msg_off, \
    server_msg_off = request_trade_subscription(client, msg_id, 
                               sub_scope=SUBSCRIPTION_SCOPE_ACCOUNT_SUMMARY,
                               subscribe=False)
    
    logger.info(f'9. Sent request_trade_subscription for {symbol1}')
    
    # 10. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’.
    print('server_msg_off', server_msg_off)
    assert status_msg_off.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'10. request_trade_subscription for {symbol1}: SUCCESS')

    # 11. Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT.logoff()
    logger.info(f'11. Send Logoff message')

    CONNECT.disconnect()
    logger.info('11. Logoff')
    logger.info('========(End test_account_summary_status_requests)========') 
    

    
def get_history_orders():
    
    #client, msg_id, account_id, from_date, to_date
    client = webapi_client.WebApiClient()
    client.connect(host_name)
    client_msg, logon_obj, logon_server_msg = logon(client, user_name, password)
    
    from_date = datetime.datetime(2025,7,22,0,0,0, tzinfo=timezone.utc) 
    to_date = datetime.datetime.now(timezone.utc) #+ datetime.timedelta(seconds=2)
    request_historical_orders(client, int(random_string(length=7)),
                              account_id, from_date, to_date)
    logoff_obj, logoff_server_msg = logoff(client)
    #logger.info('Logoff')

    client.disconnect()

if True:
    goflat() # Initialisation for the whole account
    
    print('====Test New order')
    #test_success_order_requests() # tested (stablised)
    
    print('====Test modify order')
    #test_modify_order() # tested (stablised)
                         # qty change (attribute problem)
                         # LMT price change tested (stablised)
                         # Stp price change tested (stablised)
                         
    print('====Test Cancel order')
    #test_cancel_order() # tested (Stablised)
    print('====Test suspend activate order')
    #test_suspended_activate_order() # tested (Stablised)
    print('====Test position status')
    #test_success_pos_status_requests() #tested (Stablised)
    #test_success_collateral_status_requests() #tested (Stablised)   
    #time.sleep(5)
    print('====Test account summary')

    #test_account_summary_status_requests() # tested (Stablised)
    print('====get_history_orders')
    logger.info("=============================================================")
    #get_history_orders() # to Check the active orders after the test
    
