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

#from WebAPI.webapi_2_pb2 import *
from WebAPI import webapi_client
from WebAPI.user_session_2_pb2 import LogonResult
from WebAPI.metadata_2_pb2 import ContractMetadata, SymbolResolutionReport
from WebAPI.trade_routing_2_pb2 import TradeSubscriptionStatus
from EC_API.connect.base import ConnectCQG
# =============================================================================
# from run_API_access import (
#     logon, logoff, resolve_symbol, 
#     request_trade_subscription, new_order_request,
#     random_string, cancel_order_request, modify_order_request,
#     goflat_order_request, request_historical_orders, activate_order_request
# )
# 
# =============================================================================

host_name = 'wss://demoapi.cqg.com:443'
user_name = 'EulerWAPI'
password = 'WAPI'

# Account_id and initial parameters
account_id = 17819227 # change the value according to your account_id
contract_id = 1
cl_order_id = '1' # every order must have unique cl_order_id per trader per day
order_type = 1 # 1 means MKT 2 means LMT 3 means STP 4 means STL
duration = 1
side = 1 # 1 means buy and 2 means sell
qty_significant = 1
qty_exponent = 0
is_manual = False


from EC_API.ordering.enums import SUBSCRIPTION_SCOPE_ORDERS


trade_subscription_id = 1
request_id = 1 # request id must have unique value per trader per day




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


def test_new_order_request_SELL_MKT_DAY() -> None:
    return

def test_new_order_request_BUY_MKT_GTC() -> None:
    return 

def test_new_order_request_SELL_MKT_FAK() -> None:
    return

def test_new_order_request_BUY_LMT_DAY() -> None:
    return

def test_new_order_request_SELL_LMT_GTD() -> None:
    return

def test_new_order_request_BUY_LMT_GTC_ICEBERG() -> None:
    return

def test_new_order_request_SELL_LMT_DAY_FUNARI() -> None:
    return

def test_new_order_request_BUY_STP_GTC() -> None:
    return
def test_new_order_request_BUY_STP_GTD_TRAIL() -> None:
    return
def test_new_order_request_SELL_STP_DAY_QT() -> None:
    return
def test_new_order_request_BUY_STL_DAY_TRAIL_QT() -> None:
    return

def test_new_order_request_SELL_STL_GTD() -> None:
    return




def test_success_order_requests() -> None:
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_success_order_requests)========')

    # 1.Send Logon message with valid credentials.
    logger.info('1.Send Logon message with valid credentials.')

    client_msg, logon_obj, logon_server_msg = CONNECT.logon()

    print('logon_server_msg', logon_server_msg)
    # 2.Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')

    # 3. Send InformationRequest with symbol_resolution_requests for the \
    # symbols Symbol1, Symbol2, Symbol3.
    symbol1 = "ZUC"
    msg_id = int(random_string(length=5))
    information_request1, server_msg1 = resolve_symbol(client, symbol1, msg_id)
    logger.info(f'-------(3. Start Testing orders with Symbol1: {symbol1})--------')
    logger.info(f'3. Send InformationRequest with symbol_resolution_requests for Symbol1: {symbol1}')
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

    print('step 4 successful')

    # 5. Send TradeSubscription with subscribe = true and 
    # subscription_scope=ORDERS.
    trade_sub_request1, status_msg1, trade_server_msg1 = request_trade_subscription(client, msg_id)

    print('trade_sub_request',trade_sub_request1)
    print('server_msg', server_msg1)
    logger.info(f'5. Send TradeSubscription with subscribe = true and subscription_scope=ORDERS.')

    print('step 5 successful')

    # 6. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’, 
    # OrderStatus with any orders according to PublicationType(ACCOUNT, 
    # SALES_SERIES, BROKERAGE and ALL_AUTHORIZED), and TradeSnapshotCompletion.
    
    print('trade_server_msg1', trade_server_msg1.trade_subscription_statuses)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. request_trade_subscription for {symbol1}: SUCCESS')
    print('6. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’')

    # 7. For the following tests, use the order types the application being 
    # certified is going to use.
    
    # 8.  Send NewOrder for SELL MKT DAY order for Symbol1.(Written)
    logger.info('-----------------------------------')
    logger.info(f'8. Send NewOrder for SELL MKT DAY order for Symbol1: {symbol1}')

    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    print('-----------------------------------')    
    server_msg_NO_SELL_MKT_DAY_SYM1 =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_DAY, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual)
    # 9.  Receive OrderStatus.
    assert server_msg_NO_SELL_MKT_DAY_SYM1.order_statuses[-1].order.order_type == ORDER_TYPE_MKT #(1)
    assert server_msg_NO_SELL_MKT_DAY_SYM1.order_statuses[-1].order.duration == DURATION_DAY #(1)
    assert server_msg_NO_SELL_MKT_DAY_SYM1.order_statuses[-1].order.side == SIDE_SELL #(2)
    logger.info(f'9. Receive OrderStatus: {server_msg_NO_SELL_MKT_DAY_SYM1.order_statuses}')
    print('step 9 successful')

    
    # 10. Send NewOrder for BUY MKT GTC order for Symbol1.(Written)
    logger.info('-----------------------------------')
    logger.info(f'10. Send NewOrder for BUY MKT GTC order for Symbol1: {symbol1}')

    print('-----------------------------------')    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_BUY_MKT_GTC_SYM1 =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_GTC, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual)
    time.sleep(4)

    print("server_msg_NO_BUY_MKT_GTC_SYM1", server_msg_NO_BUY_MKT_GTC_SYM1, len(server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses))
    print("ORDER_TYPE_MKT, DURATION_GTC, SIDE_BUY,", ORDER_TYPE_MKT, DURATION_GTC, SIDE_BUY,)
    print("cl_order_id, [-1]cl_order_id", cl_order_id, server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses[-1].order.cl_order_id)
    print('step 10 successful')

    # 11. Receive OrderStatus.
    assert server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses[-1].order.order_type == ORDER_TYPE_MKT
    assert server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses[-1].order.duration == DURATION_GTC
    assert server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses[-1].order.side == SIDE_BUY
    logger.info(f'11. Receive OrderStatus: {server_msg_NO_BUY_MKT_GTC_SYM1.order_statuses}')
    print('step 11 successful')

    
    # 12. Send NewOrder for SELL MKT FAK order for Symbol1.(Written)
    logger.info('-----------------------------------')
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    print('-----------------------------------')
    logger.info(f'12. Send NewOrder for SELL MKT FAK order for Symbol1: {symbol1}')

    server_msg_NO_SELL_MKT_FAK_SYM1 =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_MKT, 
                                        DURATION_FAK, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual)
    time.sleep(4)

    print("server_msg_NO_SELL_MKT_FAK_SYM1", server_msg_NO_SELL_MKT_FAK_SYM1, 
          len(server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses))
    print("ORDER_TYPE_MKT, DURATION_FAK, SIDE_SELL", ORDER_TYPE_MKT, DURATION_FAK, SIDE_SELL)
    print("cl_order_id, [-1]cl_order_id", cl_order_id, 
          server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses[-1].order.cl_order_id)

    print('step 12 successful')

    # 13. Receive OrderStatus.
    assert server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses[-1].order.order_type == ORDER_TYPE_MKT
    assert server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses[-1].order.duration == DURATION_FAK
    assert server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses[-1].order.side == SIDE_SELL
    logger.info(f'13. Receive OrderStatus: {server_msg_NO_SELL_MKT_FAK_SYM1.order_statuses}')
    print('step 13 successful')
    
    #################### Test Symbol 2 #################3
    symbol2 = "HOE"
    SCALED_LIMIT_PRICE2 = 27000
    information_request2, server_msg2 = resolve_symbol(client, symbol2, 200)
    logger.info(f'-------(Start Testing orders with Symbol2: {symbol2})--------')
    print('server_msg2.information_reports',server_msg2.information_reports)
    
    assert server_msg2.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'Information Report for {symbol2} status_code: SUCCESS')
    
    contract_metadata2 = server_msg2.information_reports[0].symbol_resolution_report.contract_metadata
    assert type(contract_metadata2)==ContractMetadata
    logger.info(f'Contract_metadata for {symbol2}: {contract_metadata2}')
    print("Step 17 success")

    trade_sub_request2, status_msg2, server_msg2 = request_trade_subscription(client, 2000)
    assert status_msg2.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS

    CONTRACT_ID_SYM2 = contract_metadata2.contract_id
    
    # 14. Send NewOrder for BUY LMT DAY order for Symbol2.
    logger.info('-----------------------------------')
    logger.info(f'14. Send NewOrder for BUY LMT DAY order for Symbol2: {symbol2}')
    print('-----------------------------------')
    print('server_msg_NO_BUY_LMT_DAY_SYM2')
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_BUY_LMT_DAY_SYM2 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM2, 
                                        cl_order_id, ORDER_TYPE_LMT, 
                                        DURATION_DAY, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_LIMIT_PRICE2)
    request_id += 1

    # 15. Receive OrderStatus.
    logger.info(f'15. Receive OrderStatus: {server_msg_NO_BUY_LMT_DAY_SYM2.order_statuses}')
    assert server_msg_NO_BUY_LMT_DAY_SYM2.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
    assert server_msg_NO_BUY_LMT_DAY_SYM2.order_statuses[-1].order.duration == DURATION_DAY
    assert server_msg_NO_BUY_LMT_DAY_SYM2.order_statuses[-1].order.side == SIDE_BUY
    print("Step 15 success")

    # 16. Send NewOrder for SELL LMT GTD order for Symbol2.
    logger.info('-----------------------------------')
    logger.info(f'16. Send NewOrder for SELL LMT GTD order for Symbol2: {symbol2}.')
    print('-----------------------------------')
    print('server_msg_NO_SELL_LMT_GTD_SYM2')
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    GOOD_THRU_DATE = int((datetime.datetime.now(timezone.utc) + datetime.timedelta(days=1)).timestamp())

    server_msg_NO_SELL_LMT_GTD_SYM2 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM2, 
                                        cl_order_id, ORDER_TYPE_LMT, 
                                        DURATION_GTD, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        good_thru_date=GOOD_THRU_DATE,
                                        scaled_limit_price=SCALED_LIMIT_PRICE2)
    

    # 17. Receive OrderStatus.
    assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
    assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.duration == DURATION_GTD
    assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.side == SIDE_SELL
    logger.info(f'17. Receive OrderStatus: {server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses}')


    print("Step 17 success")
    # 18. Send NewOrder for BUY LMT GTC ICEBERG order for Symbol2.
    logger.info('-----------------------------------')
    logger.info('Test SELL_LMT_GTC_ICEBERG_SYM2')
    print('-----------------------------------')
    print('server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM2, 
                                        cl_order_id, ORDER_TYPE_LMT, 
                                        DURATION_GTC, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_LIMIT_PRICE2,
                                        exec_instructions=EXEC_INSTRUCTION_ICEBERG)

    # 19. Receive OrderStatus.
    assert server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
    assert server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2.order_statuses[-1].order.duration == DURATION_GTC
    assert server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2.order_statuses[-1].order.side == SIDE_BUY
    assert server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_ICEBERG
    logger.info(f'19. Receive OrderStatus: {server_msg_NO_SELL_LMT_GTC_ICEBERG_SYM2.order_statuses}')
    print("Step 19 success")

    # 20. Send NewOrder for SELL LMT DAY FUNARI order for Symbol2. 
    logger.info('-----------------------------------')
    logger.info(f'20. Send NewOrder for SELL LMT DAY FUNARI order for Symbol2: {symbol2}')
    print('-----------------------------------')
    print('server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2 =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_LMT, 
                                        DURATION_DAY, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_LIMIT_PRICE2,
                                        exec_instructions = EXEC_INSTRUCTION_FUNARI)

    # 21. Receive OrderStatus.
    assert server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
    assert server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2.order_statuses[-1].order.duration == DURATION_DAY
    assert server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2.order_statuses[-1].order.side == SIDE_SELL
    assert server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_FUNARI
    logger.info(f'21. Receive OrderStatus: {server_msg_NO_SELL_LMT_DAY_FUNARI_SYM2.order_statuses}')


    # 22. Send NewOrder for BUY STP GTC order for Symbol3.
    symbol3 = "CLE"
    SCALED_STOP_PRICE3 = 6300
    information_request3, server_msg3 = resolve_symbol(client, symbol3, 300)

    logger.info(f'-------(Start Testing orders with Symbol3: {symbol3})--------')

    assert server_msg3.information_reports[0].status_code == InformationReport.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'Information Report for {symbol3} status_code: SUCCESS')

    contract_metadata3 = server_msg3.information_reports[0].symbol_resolution_report.contract_metadata
    assert type(contract_metadata3)==ContractMetadata
    logger.info(f'Contract_metadata for {symbol3}: {contract_metadata3}')
    
    CONTRACT_ID_SYM3 = contract_metadata3.contract_id
    
    trade_sub_request3, status_msg3, server_msg3 = request_trade_subscription(client, 3000)
    assert status_msg3.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS

    logger.info('-----------------------------------')
    logger.info('22. Send NewOrder for BUY STP GTC order for Symbol3: {symbol3]')
    print('-----------------------------------')
    print('server_msg_NO_BUY_STP_GTC_SYM3')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_BUY_STP_GTC_SYM3 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM3, 
                                        cl_order_id, ORDER_TYPE_STP, 
                                        DURATION_GTC, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_stop_price=SCALED_STOP_PRICE3)

    # 23. Receive OrderStatus.
    assert server_msg_NO_BUY_STP_GTC_SYM3.order_statuses[-1].order.order_type == ORDER_TYPE_STP
    assert server_msg_NO_BUY_STP_GTC_SYM3.order_statuses[-1].order.duration == DURATION_GTC
    assert server_msg_NO_BUY_STP_GTC_SYM3.order_statuses[-1].order.side == SIDE_BUY
    logger.info(f'23. Receive OrderStatus: {server_msg_NO_BUY_STP_GTC_SYM3.order_statuses}')

    # 24. Send NewOrder for BUY STP GTD TRAIL order for Symbol3.
    logger.info('-----------------------------------')
    logger.info('24. Send NewOrder for BUY STP GTD TRAIL order for Symbol3: {symbol3}')
    print('-----------------------------------')
    print('server_msg_NO_BUY_STP_GTD_TRAIL_SYM3')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    GOOD_THRU_DATE = int((datetime.datetime.now(timezone.utc) + datetime.timedelta(days=1)).timestamp())

    server_msg_NO_BUY_STP_GTD_TRAIL_SYM3 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM3, 
                                        cl_order_id, ORDER_TYPE_STP, 
                                        DURATION_GTD, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        exec_instructions = EXEC_INSTRUCTION_TRAIL,
                                        good_thru_date=GOOD_THRU_DATE,
                                        scaled_stop_price=SCALED_STOP_PRICE3,
                                        scaled_trail_offset = 10)

    # 25. Receive OrderStatus.
    assert server_msg_NO_BUY_STP_GTD_TRAIL_SYM3.order_statuses[-1].order.order_type == ORDER_TYPE_STP
    assert server_msg_NO_BUY_STP_GTD_TRAIL_SYM3.order_statuses[-1].order.duration == DURATION_GTD
    assert server_msg_NO_BUY_STP_GTD_TRAIL_SYM3.order_statuses[-1].order.side == SIDE_BUY
    logger.info(f'OrderStatus: {server_msg_NO_BUY_STP_GTD_TRAIL_SYM3.order_statuses}')

    # 26. Send NewOrder for SELL STP DAY QT order for Symbol3.
    logger.info('-----------------------------------')
    logger.info('26. Send NewOrder for SELL STP DAY QT order for Symbol3: {symbol3}')
    print('-----------------------------------')
    print('server_msg_NO_SELL_STP_DAY_QT_SYM3')
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_SELL_STP_DAY_QT_SYM3 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM3, 
                                        cl_order_id, ORDER_TYPE_STP, 
                                        DURATION_DAY, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_stop_price=SCALED_STOP_PRICE3)

    # 27. Receive OrderStatus.
    assert server_msg_NO_SELL_STP_DAY_QT_SYM3.order_statuses[-1].order.order_type == ORDER_TYPE_STP
    assert server_msg_NO_SELL_STP_DAY_QT_SYM3.order_statuses[-1].order.duration == DURATION_DAY
    assert server_msg_NO_SELL_STP_DAY_QT_SYM3.order_statuses[-1].order.side == SIDE_SELL
    logger.info(f'27. Receive OrderStatus: {server_msg_NO_SELL_STP_DAY_QT_SYM3.order_statuses}')

    # 28. Send NewOrder for BUY STL DAY TRAIL QT order for Symbol3.
    logger.info('-----------------------------------')
    logger.info('28. Send NewOrder for BUY STL DAY TRAIL QT order for Symbol3: {symbol3}')
    print('-----------------------------------')
    print('server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)

    server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM3, 
                                        cl_order_id, ORDER_TYPE_STL, 
                                        DURATION_DAY, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_STOP_PRICE3+300,
                                        scaled_stop_price=SCALED_STOP_PRICE3,
                                        exec_instructions = EXEC_INSTRUCTION_TRAIL,
                                        scaled_trail_offset = 10)

    # 29. Receive OrderStatus.
    assert server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3.order_statuses[-1].order.order_type == ORDER_TYPE_STL
    assert server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3.order_statuses[-1].order.duration == DURATION_DAY
    assert server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3.order_statuses[-1].order.side == SIDE_BUY
    assert server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_TRAIL
    logger.info(f'29. Receive rderStatus: {server_msg_NO_BUY_STL_DAY_QT_TRAIL_QT_SYM3.order_statuses}')

    # 30. Send NewOrder for SELL STL GTD order for Symbol3.
    logger.info('-----------------------------------')
    logger.info('30. Send NewOrder for SELL STL GTD order for Symbol3: {symbol3}')
    print('-----------------------------------')
    print('server_msg_NO_SELL_STL_DAY_QT_TRAIL_QT_SYM3')
    
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    
    GOOD_THRU_DATE = int((datetime.datetime.now(timezone.utc) + datetime.timedelta(days=1)).timestamp())

    server_msg_NO_SELL_STL_GTD_SYM3 =  new_order_request(
                                        client, request_id, 
                                        account_id, CONTRACT_ID_SYM3, 
                                        cl_order_id, ORDER_TYPE_STL, 
                                        DURATION_GTD, SIDE_SELL, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_STOP_PRICE3-300,
                                        scaled_stop_price=SCALED_STOP_PRICE3,
                                        good_thru_date = GOOD_THRU_DATE) 

    
    # 31. Receive OrderStatus.
    assert server_msg_NO_SELL_STL_GTD_SYM3.order_statuses[-1].order.order_type == ORDER_TYPE_STL
    assert server_msg_NO_SELL_STL_GTD_SYM3.order_statuses[-1].order.duration == DURATION_GTD
    assert server_msg_NO_SELL_STL_GTD_SYM3.order_statuses[-1].order.side == SIDE_SELL
    logger.info(f'31. Receive OrderStatus: {server_msg_NO_SELL_STL_GTD_SYM3.order_statuses}')

    # 32. Send TradeSubscription with subscribe = false.
    print("32. Send TradeSubscription with subscribe = false")
    trade_sub_request_unsub, status_msg_unsub, \
    trade_server_msg_unsub = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_ORDERS,
                                                   subscribe= False)
    logger.info(f'32. Send TradeSubscription with subscribe = false')
    

    # 33. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’.
    assert status_msg_unsub.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'33. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’')

    # 34. Send TradeSubscription with subscribe = true.
    trade_sub_request_sub, status_msg_sub, \
    trade_server_msg_sub = request_trade_subscription(client, msg_id, 
                                                   sub_scope=SUBSCRIPTION_SCOPE_ORDERS,
                                                   subscribe= True)
    logger.info('34. Send TradeSubscription with subscribe = true')
    
    
    # 35. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’, 
    # all orders placed above with their statuses, and TradeSnapshotCompletion.
    assert status_msg_sub.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info('35. Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’')
    logger.info(f'35. TradeSubscriptionStatus: {trade_server_msg_sub}')
    
    # 36. Send Logoff message.
    logger.info('36. Send Logoff message')

    logoff_obj, logoff_server_msg = CONNECT.logoff()
    CONNECT.disconnect()
    logger.info('========(End test_success_order_requests)========') 
    
    # 37. Partially repeat this test for all TradeSubscription PublicationTypes 
    # the application being certified is going to use. The customers are 
    # encouraged to use wider publication types where applicable, e.g. 
    # not subscribing to trades for every account, but subscribing for 
    # “all authorized” instead.
    # 
    # 38. Partially repeat this test with different instrument types: 
    # an option (e.g. C.EP, P.EP), some strategies (EDAB2,), an equity (S.MSFT).
    
    return 


def test_modify_order()-> None:
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


def test_cancel_order() -> None:
    # Cancel Order
    CONNECT = ConnectCQG(host_name,user_name, password)
    logger.info('========(Start test_cancel_order)========')

    # 1.  Send Logon message with valid credentials.
    client_msg, logon_obj, logon_server_msg = CONNECT.logon()
    logger.info('1. Send Logon message with valid credentials.')

    print('logon_server_msg', logon_server_msg)
    # 2.  Receive LogonResult with result_code='SUCCESS'.
    assert logon_server_msg.logon_result.result_code == LogonResult.ResultCode.RESULT_CODE_SUCCESS
    logger.info('2. LogonResult result_code: SUCCESS')
    print('step 2 successful')
    
    # 3. Send InformationRequest with symbol_resolution_requests for the \
    # symbols symbol=’F.US.ZUC’.
    symbol1 = "F.US.ZUC"
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
    print('step 4 successful')

    # 5.  Send TradeSubscription with subscribe = true and subscription_scope=ORDERS.
    trade_sub_request1, status_msg1, trade_server_msg1 = request_trade_subscription(client, 
                                                                       msg_id, 
                                                                       sub_scope=SUBSCRIPTION_SCOPE_ORDERS)    
    print('trade_sub_request',trade_sub_request1)
    print('server_msg', trade_server_msg1)
    print('step 5 successful')
    
    # 6.  Receive TradeSubscriptionStatus with status_code = ‘SUCCESS’,\
    # and TradeSnapshotCompletion.
    print('trade_server_msg1', trade_server_msg1.trade_subscription_statuses)
    
    assert status_msg1.trade_subscription_statuses[0].status_code == TradeSubscriptionStatus.StatusCode.STATUS_CODE_SUCCESS
    logger.info(f'6. request_trade_subscription for {symbol1}: SUCCESS')

    print('step 6 successful')
    # 7.  Send NewOrder for BUY LMT DAY order.
    request_id = int(random_string(length=7))
    cl_order_id = str(request_id)
    SCALED_LIMIT_PRICE = 70000
    print('cl_order_id', cl_order_id)
    logger.info(f'7. Send new BUY DAY LMT order for {symbol1} at {SCALED_LIMIT_PRICE}')
    server_msg_NO_BUY_LIMIT_DAY =  new_order_request(
                                        client, request_id, 
                                        account_id, contract_id, 
                                        cl_order_id, ORDER_TYPE_LMT, 
                                        DURATION_DAY, SIDE_BUY, 
                                        qty_significant, qty_exponent, 
                                        is_manual,
                                        scaled_limit_price=SCALED_LIMIT_PRICE)
    print('server_msg_NO_BUY_LIMIT_DAY', server_msg_NO_BUY_LIMIT_DAY)

    ORDER_ID = server_msg_NO_BUY_LIMIT_DAY.order_statuses[0].order_id
    print("ORDER_ID", ORDER_ID)
    print('Step 7 successful')
    
    # 8.  Receive OrderStatus.
    #assert 
    #print('server_msg_NO_BUY_LIMIT_DAY', server_msg_NO_BUY_LIMIT_DAY)
    logger.info(f'8. Receive OrderStatus for {symbol1}')

    # 9.  Send CancelOrder.
    print('NEW ORDER cl_order_id', cl_order_id, type(cl_order_id))
    orig_cl_order_id = cl_order_id
    cl_order_id = str(request_id+10)
    print('CANCEL ORDER orig_cl_order_id', orig_cl_order_id, type(orig_cl_order_id))
    #request_id = request_id + 10
    #cl_order_id = str(request_id +10)
    print('CANCEL ORDER cl_order_id', cl_order_id, type(cl_order_id))
    #order_id = '900' #server_msg_NO_BUY_LIMIT_DAY.order_statuses[0].order_id

    corder_request, server_msg_cancel = cancel_order_request(client, request_id, 
                                                             account_id, ORDER_ID, 
                                                             orig_cl_order_id, 
                                                             cl_order_id)
    logger.info(f'9. Send CancelOrder for {symbol1}')

    # 10. Receive OrderStatus.
    print('corder_request', corder_request)
    print('server_msg_cancel', server_msg_cancel)
    logger.info(f'10. Receive OrderStatus for Cancel Order: {server_msg_cancel}')

    # 11. Send Logoff message.
    logoff_obj, logoff_server_msg = CONNECT.logoff()
    logger.info('11. Send Logoff message.')

    CONNECT.disconnect()
    print('Step 11 successful')

    logger.info('========(End test_cancel_order)========') 
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
    
