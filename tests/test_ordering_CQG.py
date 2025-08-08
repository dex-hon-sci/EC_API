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

from tests.ordering_cases import (
    NewOrderCases, 
    ModifyOrderCases, 
    CancelOrderCases,
    ActivateOrderCases
    )
        
@pytest.mark.parametrize() 
def test_success_order_requests(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    #logger.info('========(Start test_success_order_requests)========')
    # 1.Send Logon message with valid credentials.
    #logger.info('1.Send Logon message with valid credentials.')
    NOC = NewOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    NOC.run_all()
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()
    
@pytest.mark.parametrize() 
def test_modify_order(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    MOC = ModifyOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    MOC.run_all()
    logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()

    
@pytest.mark.parametrize() 
def test_cancel_order(symbol_name: str) -> None:
    CONNECT = ConnectCQG(HOST_NAME, USR_NAME, PASSWORD)
    COC = CancelOrderCases(CONNECT, ACCOUNT_ID, symbol_name)
    COC.run_all()
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

def test_modify_order() -> None:
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_modify_order)========')

    # 1. Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()
    logger.info('1. Send Logon message with valid credentials.')

    print('logon_server_msg', logon_server_msg)
    # 2. Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. Receive LogonResult result_code: SUCCESS')

    # 3. Send InformationRequest with symbol_resolution_request for 
    symbol1 = "F.US.ZUI"
    information_request1, server_msg1 = resolve_symbol(client, symbol1, 1)
    msg_id = 4
    logger.info(f'-------(Start Testing orders with Symbol1: {symbol1})--------')
    logger.info('3. Send InformationRequest with symbol_resolution_request')

    # 4. Receive InformationReport with SymbolResolutionReport with 
    # status_code=’SUCCESS’ and contract_metadata for the symbol.
    assert server_msg1.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    contract_metadata1 = server_msg1.information_reports[0].symbol_resolution_report.contract_metadata

    assert type(contract_metadata1)==ContractMetadata
    logger.info(f'4. Information Report for {symbol1} status_code: SUCCESS')
    logger.info(f'4. Contract_metadata for {symbol1}: {contract_metadata1}')

    # 5. Send TradeSubscription with subscribe = true and subscription_scope=ORDERS.
    trade_sub_request1, status_msg1, trade_server_msg1 = request_trade_subscription(
                                                                       client, 
                                                                       msg_id, 
                                                                       sub_scope=SUBSCRIPTION_SCOPE_ORDERS)    
    msg_id +=1
    print('trade_sub_request',trade_sub_request1)
    print('server_msg', trade_server_msg1)
    print('step 5 successful')
    logger.info(f'5. Send TradeSubscription with subscribe = true and subscription_scope=ORDERS')

    # 6. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’ 
    # and TradeSnapshotCompletion.
    print('trade_server_msg1', trade_server_msg1.trade_subscription_statuses)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. Receive TradeSubscriptionStatus for {symbol1}: SUCCESS')

    print('step 6 successful')

    # 7. Send NewOrder for SELL STL GTC order.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    SCALED_STP_PRICE = 9000
    SCALED_LMT_PRICE = 10000
    
    logger.info(f'7. Send new SELL STL GTC order for {symbol1} at {SCALED_STP_PRICE}')
    server_msg_NO_SELL_STL_GTC =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_STL, 
                                        DURATION_GTC, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_LMT_PRICE,
                                        scaled_stop_price=SCALED_STP_PRICE)
    ORDER_ID = server_msg_NO_SELL_STL_GTC.order_statuses[0].order_id

    print('Step 7 successful')
    
    # 8.  Receive OrderStatus.
    print('server_msg_NO_SELL_STL_GTC', server_msg_NO_SELL_STL_GTC)
    print(server_msg_NO_SELL_STL_GTC.order_statuses[0].order_id)
    logger.info(f'8. Receive OrderStatus: {server_msg_NO_SELL_STL_GTC}')

    orig_cl_order_id = cl_order_id

# =============================================================================
#     # 9. Send ModifyOrder with modified qty.
#     request_id = int(random_string(length=7))
#     orig_cl_order_id = cl_order_id
#     cl_order_id = str(request_id +10)
#     print('MODIFY ORDER orig_cl_order_id', orig_cl_order_id)
#     #request_id = request_id + 10
#     #cl_order_id = str(request_id +10)
#     print('MODIFY ORDER cl_order_id', cl_order_id)
#     
#     new_qty = 7
#     #new_qty = Decimal(significand=1)
#     print("new_qty", new_qty)
#     server_msg_modify1 = modify_order_request(client, request_id, account_id, 
#                                               ORDER_ID, orig_cl_order_id, 
#                                               cl_order_id, qty = new_qty)
# 
#     # 10. Receive OrderStatus.
#     print('server_msg_modify 1', server_msg_modify1)
# =============================================================================
    
    # 11. Send ModifyOrder with modified limit_price.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id +10)
    print('MODIFY ORDER orig_cl_order_id', orig_cl_order_id)
    print('MODIFY ORDER cl_order_id', cl_order_id)
    logger.info(f'11. Send ModifyOrder with modified limit_price: 10000->11000')
    server_msg_modify2 = modify_order_request(client, request_id, account_id, 
                                              ORDER_ID, orig_cl_order_id, 
                                              cl_order_id, scaled_limit_price = 11000)

    # 12. Receive OrderStatus.
    print('server_msg_modify2', server_msg_modify2)
    logger.info(f'12. Receive OrderStatus: {server_msg_modify2}')


    # 13. Send ModifyOrder with modified stop_price.
    #cl_order_id = str(request_id +10)
    request_id = int(random_string(length=7))
    #orig_cl_order_id = cl_order_id
    cl_order_id = str(request_id +10)
    print('MODIFY ORDER orig_cl_order_id', orig_cl_order_id)
    print('MODIFY ORDER cl_order_id', cl_order_id)
    logger.info(f'11. Send ModifyOrder with modified stop_price: 9000->8000')
    server_msg_modify3 = modify_order_request(client, request_id, account_id, 
                                              ORDER_ID, orig_cl_order_id, 
                                              cl_order_id, scaled_stop_price = 8000)

    # 14. Receive OrderStatus.
    print('server_msg_modify3', server_msg_modify3)
    logger.info(f'14. Receive OrderStatus: {server_msg_modify3}')

    # 15. Send Logoff message.
    logger.info(f'15. Send Logoff message')

    logoff_obj, logoff_server_msg = CONNECT.logoff()

    CONNECT.disconnect()
    logger.info('========(End test_modify_order)========') 
    return 

    
def test_suspended_activate_order() -> None:
    # Place a Suspended Order, Activate Order
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_suspended_activate_order)========')

    # 1.  Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()

    print('logon_server_msg', logon_server_msg)

    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')

    # 3.  Send InformationRequest with symbol_resolution_request for symbol=’F.US.ZUC’.
    symbol1 = "F.US.ZUC"
    msg_id = int(random_string(length=5))
    information_request1, server_msg1 = resolve_symbol(client, symbol1, msg_id)
    print('step 3 successful')
    logger.info('3. Send InformationRequest with symbol_resolution_request for symbol=’F.US.ZUC’.')

    msg_id +=1
    
    # 4.  Receive InformationReport with SymbolResolutionReport with 
    #status_code=’SUCCESS’ and contract_metadata for the symbol.
    assert server_msg1.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info('4. Receive InformationReport with SymbolResolutionReport with \
                 status_code=’SUCCESS’ and contract_metadata for the symbol')

    # 5.  Send TradeSubscription with subscribe = true and subscription_scope=ORDERS.
    trade_sub_request1, status_msg1, \
    trade_server_msg1 = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_ORDERS)    
    logger.info(f'5. Send TradeSubscription with subscribe = true and subscription_scope=ORDERS.')

    # 6.  Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’ and 
    # TradeSnapshotCompletion.
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. Receive TradeSubscriptionStatus with status_code for {symbol1}: SUCCESS')

    # 7.  Send NewOrder for SELL LMT DAY order with suspend = true.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    logger.info(f'7. Send NewOrder SELL DAY MKT order for {symbol1}')
    server_msg_SELL_MKT_DAY =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_DAY, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        sub_scope=SUBSCRIPTION_SCOPE_ORDERS,
                                        suspend=True)
    logger.info(f'7. Send NewOrder for SELL LMT DAY order with suspend = true.')

    # 8.  Receive OrderStatus.
    assert server_msg_SELL_MKT_DAY.order_statuses[0].status == SUSPENDED
    logger.info(f'8. Receive OrderStatus: {server_msg_SELL_MKT_DAY}')
    
    ORDER_ID = server_msg_SELL_MKT_DAY.order_statuses[0].order_id

    # 9.  Send ActivateOrder.
    orig_cl_order_id = cl_order_id
    cl_order_id = str(request_id+10)
    server_msg_activate = activate_order_request(client, request_id, 
                                                 account_id, ORDER_ID, 
                                                 orig_cl_order_id, cl_order_id)

    print("server_msg_activate", server_msg_activate)
    logger.info(f'9. Send ActivateOrder.')

    # 10. Receive OrderStatus.
    
    logger.info(f' 10. Receive OrderStatus: {server_msg_activate}')
    # 11. Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT.logoff()
    logger.info(f'11. Send Logoff message.')

    CONNECT.disconnect()
    logger.info('========(End test_suspended_activate_order)========') 
    
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
    
