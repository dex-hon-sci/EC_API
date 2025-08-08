#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 11:02:05 2025

@author: dexter
"""

from EC_API.connect.base import ConnectCQG
from EC_API.utility.base import random_string
#from EC_API.ordering.enums import SUBSCRIPTION_SCOPE_ORDERS, RequestType
from EC_API.ordering.enums import *
from EC_API.ordering.CQG_LiveOrder import CQGLiveOrder


class NewOrderCases(object):
    """
    Test cases for New order requests.
    """
    def __init__(self, 
                 connect: ConnectCQG, 
                 account_id: int,
                 symbol_name: str):
        self.connect = connect
        self.account_id = account_id
        #self.contract_id = None
        self.symbol_name = symbol_name
        
    def new_order_request_SELL_MKT_DAY(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_MKT,
            "duration": DURATION_DAY, 
            "side": SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            }
        
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
        
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_MKT #(1)
        assert server_msg.order_statuses[-1].order.duration == DURATION_DAY #(1)
        assert server_msg.order_statuses[-1].order.side == SIDE_SELL #(2)
    
    def new_order_request_BUY_MKT_GTC(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_MKT,
            "duration": DURATION_GTC, 
            "side": SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
    
            }
        
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string()), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
        
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_MKT
        assert server_msg.order_statuses[-1].order.duration == DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
    
    def new_order_request_SELL_MKT_FAK(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_MKT,
            "duration": DURATION_FAK, 
            "side": SIDE_SELL,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            }
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                     request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_MKT
        assert server_msg.order_statuses[-1].order.duration == DURATION_FAK
        assert server_msg.order_statuses[-1].order.side == SIDE_SELL
    
    def new_order_request_BUY_LMT_DAY(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_LMT,
            "duration": DURATION_DAY, 
            "side": SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                     request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
    
    
    def new_order_request_SELL_LMT_GTD(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_LMT,
            "duration": DURATION_GTD, 
            "side": SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "good_thru_date": GOOD_THRU_DATE,
            "scaled_limit_price": scaled_limit_price
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string()), 
                               account_id = self.account_id)
        CLOrder.send(request_type=RequestType.NEW_ORDER, 
                     request_details = request_details)
            
    
        assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
        assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.duration == DURATION_GTD
        assert server_msg_NO_SELL_LMT_GTD_SYM2.order_statuses[-1].order.side == SIDE_SELL
    
    
    def new_order_request_BUY_LMT_GTC_ICEBERG(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_LMT,
            "duration": DURATION_GTC, 
            "side": SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            "exec_instructions": EXEC_INSTRUCTION_ICEBERG,
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_ICEBERG
    
    
    def new_order_request_SELL_LMT_DAY_FUNARI(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_LMT,
            "duration": DURATION_DAY, 
            "side": SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            "exec_instructions": EXEC_INSTRUCTION_FUNARI
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == SIDE_SELL
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_FUNARI
    
    
    def new_order_request_BUY_STP_GTC(self, scaled_stop_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_STP,
            "duration": DURATION_GTC, 
            "side": SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_stop_price": scaled_stop_price
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
    
    
    def new_order_request_BUY_STP_GTD_TRAIL(self, scaled_stop_price) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_STP,
            "duration": DURATION_GTD, 
            "side": SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "exec_instructions": EXEC_INSTRUCTION_TRAIL,
            "good_thru_date": GOOD_THRU_DATE,
            "scaled_stop_price": scaled_stop_price,
            "scaled_trail_offset": 10
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == DURATION_GTD
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
    
    
    def new_order_request_SELL_STP_DAY_QT(self, scaled_stop_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_STP,
            "duration": DURATION_DAY, 
            "side": SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_stop_price": scaled_stop_price
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
    
        # 27. Receive OrderStatus.
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == SIDE_SELL
    
    def new_order_request_BUY_STL_DAY_TRAIL_QT(self,
                                               scaled_stop_price: int,
                                               SL_price_offset: int = 300,
                                               scaled_trail_offset: int = 10) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_STL,
            "duration": DURATION_DAY, 
            "side": SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price" : SL_price_offset+SL_price_offset,
            "scaled_stop_price" : SL_price_offset,
           " exec_instructions" : EXEC_INSTRUCTION_TRAIL,
            "scaled_trail_offset": scaled_trail_offset
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        # 29. Receive OrderStatus.
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_STL
        assert server_msg.order_statuses[-1].order.duration == DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == SIDE_BUY
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == EXEC_INSTRUCTION_TRAIL
    
    
    def new_order_request_SELL_STL_GTD(self,
                                       scaled_stop_price: int,
                                       SL_price_offset: int = 300) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_STL,
            "duration": DURATION_GTD, 
            "side": SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_stop_price-SL_price_offset, 
            "scaled_stop_price": scaled_stop_price,
            "good_thru_date": GOOD_THRU_DATE
            }
    
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
            
        assert server_msg.order_statuses[-1].order.order_type == ORDER_TYPE_STL
        assert server_msg.order_statuses[-1].order.duration == DURATION_GTD
        assert server_msg.order_statuses[-1].order.side == SIDE_SELL
        
    def run_all(self) -> None:
        #Logon Info report, contrad_ID, trade Sub
        scaled_stop_price = 0
        scaled_limit_price = 0
        
        self.new_order_request_SELL_MKT_DAY()
        self.new_order_request_BUY_MKT_GTC()
        self.new_order_request_SELL_MKT_FAK()
        self.new_order_request_BUY_LMT_DAY(scaled_limit_price)
        self.new_order_request_SELL_LMT_GTD(scaled_limit_price)
        self.new_order_request_BUY_LMT_GTC_ICEBERG(scaled_limit_price)
        self.new_order_request_SELL_LMT_DAY_FUNARI(scaled_limit_price)
        self.new_order_request_BUY_STP_GTC(scaled_stop_price)
        self.new_order_request_BUY_STP_GTD_TRAIL(scaled_stop_price)
        self.new_order_request_SELL_STP_DAY_QT(scaled_stop_price)
        self.new_order_request_BUY_STL_DAY_TRAIL_QT(scaled_stop_price,
                                                    SL_price_offset = 300,
                                                    scaled_trail_offset = 10)
        self.new_order_request_SELL_STL_GTD(scaled_stop_price, SL_price_offset = 300)
        # unsub trade, logoff

class ModifyOrderCases(object):
    """
    Modify order test cases
    """
    def __init__(self, 
                 connect: ConnectCQG,
                 account_id: int,
                 symbol_name: str):
        self.connect = connect
        self.account_id = account_id
        self.symbol_name = symbol_name
        self.orig_cl_order_id = ""

    def modify_order_qty(self, new_qty: int) -> None:
    
        return
    
    def modify_order_LMT_price(self, new_LMT_price: int) -> None:
    
        return

    def modify_order_STP_price(self, new_STP_price: int) -> None:
    
        return

    def run_all(self, scaled_limit_price, scaled_stop_price) -> None:
        # Send a new order first
        initial_request_details = {
            "symbol_name": symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_MKT,
            "duration": DURATION_GTC, 
            "side": SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            "scaled_stop_price": scaled_stop_price
            }
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details)
        # Modify this order
        # self.modify_order_qty() <-decrapted 
        self.modify_order_LMT_price()
        self.modify_order_STP_price()

class CancelOrderCases(object):
    """
    Cancel order test cases
    """
    def __init__(self, 
                 connect: ConnectCQG,
                 account_id: int,
                 symbol_name: str):
        self.connect = connect
        self.account_id = account_id
        self.symbol_name = symbol_name
        self.orig_cl_order_id = ""
        
    def cancel_order(self, order_id: int) -> None:
        cancel_request_details = {
            "order_id": order_id,
            "cl_order_id": random_string(length=10),
            "orig_cl_order_id": self.orig_cl_order_id
            }
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.CANCEL_ORDER, 
                                  request_details = cancel_request_details)

        assert server_msg.order_statuses[-1].status == FILLED
        
    def run_all(self, scaled_limit_price) -> None:
        # Send a new order first
        initial_request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": ORDER_TYPE_LMT,
            "duration": DURATION_DAY, 
            "side": SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price
            }
        
        CLOrder = CQGLiveOrder(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details)
        
        ORDER_ID = server_msg.order_statuses[0].order_id
        self.orig_cl_order_id = initial_request_details['cl_order_id']

        # Cancel this order
        self.cancel_order(ORDER_ID)
        
class ActivateOrderCases(object):
    def __init__(self, 
                 connect: ConnectCQG,
                 account_id: int):
        self.connect = connect
        self.account_id = account_id
        self.orig_cl_order_id = ""
        
    def activate_order()->None:
        return 
    
    def run_all():
        return
        