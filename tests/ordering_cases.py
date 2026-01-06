#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  8 11:02:05 2025

@author: dexter
"""
from EC_API.ext.WebAPI.order_2_pb2 import GoFlatStatus
from EC_API.connect.cqg.base import ConnectCQG
from EC_API.utility.base import random_string
from EC_API.ordering.enums import (
    SubScope,
    OrderType,
    Duration,
    Side,
    RequestType,
    ExecInstruction,
    OrderStatus
    )
from EC_API.ordering.cqg.live_order import LiveOrderCQG


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
        self.symbol_name = symbol_name
        
    def new_order_request_SELL_MKT_DAY(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            }
        
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
        
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_MKT #(1)
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_DAY #(1)
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL #(2)
    
    def new_order_request_BUY_MKT_GTC(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_GTC, 
            "side": Side.SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
    
            }
        
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string()), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
        
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_MKT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
    
    def new_order_request_SELL_MKT_FAK(self) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_FAK, 
            "side": Side.SIDE_SELL,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id =int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                     request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_MKT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_FAK
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL
    
    def new_order_request_BUY_LMT_DAY(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                     request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
    
    
    def new_order_request_SELL_LMT_GTD(self, scaled_limit_price: int) -> None:
        GOOD_THRU_DATE = None
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_GTD, 
            "side": Side.SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "good_thru_date": GOOD_THRU_DATE,
            "scaled_limit_price": scaled_limit_price
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string()), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
            
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTD
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL
    
    
    def new_order_request_BUY_LMT_GTC_ICEBERG(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_GTC, 
            "side": Side.SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_ICEBERG,
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == ExecInstruction.EXEC_INSTRUCTION_ICEBERG
    
    
    def new_order_request_SELL_LMT_DAY_FUNARI(self, scaled_limit_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price,
            "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_FUNARI
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_LMT
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == ExecInstruction.EXEC_INSTRUCTION_FUNARI
    
    
    def new_order_request_BUY_STP_GTC(self, scaled_stop_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_STP,
            "duration": Duration.DURATION_GTC, 
            "side": Side.SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_stop_price": scaled_stop_price
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTC
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
    
    
    def new_order_request_BUY_STP_GTD_TRAIL(self, scaled_stop_price) -> None:
        GOOD_THRU_DATE = None
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_STP,
            "duration": Duration.DURATION_GTD, 
            "side": Side.SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "exec_instructions": ExecInstruction.EXEC_INSTRUCTION_TRAIL,
            "good_thru_date": GOOD_THRU_DATE,
            "scaled_stop_price": scaled_stop_price,
            "scaled_trail_offset": 10
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTD
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
    
    
    def new_order_request_SELL_STP_DAY_QT(self, scaled_stop_price: int) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_STP,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_stop_price": scaled_stop_price
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type = RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
    
        # 27. Receive OrderStatus.
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_STP
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL
    
    def new_order_request_BUY_STL_DAY_TRAIL_QT(self,
                                               scaled_stop_price: int,
                                               SL_price_offset: int = 300,
                                               scaled_trail_offset: int = 10) -> None:
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_STL,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_BUY,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price" : SL_price_offset+SL_price_offset,
            "scaled_stop_price" : SL_price_offset,
           " exec_instructions" : ExecInstruction.EXEC_INSTRUCTION_TRAIL,
            "scaled_trail_offset": scaled_trail_offset
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
        # 29. Receive OrderStatus.
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_STL
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_DAY
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_BUY
        assert server_msg.order_statuses[-1].order.exec_instructions[0] == ExecInstruction.EXEC_INSTRUCTION_TRAIL
    
    
    def new_order_request_SELL_STL_GTD(self,
                                       scaled_stop_price: int,
                                       SL_price_offset: int = 300) -> None:
        GOOD_THRU_DATE = None
        request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_STL,
            "duration": Duration.DURATION_GTD, 
            "side": Side.SIDE_SELL,
            "qty_significant": 2, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_stop_price-SL_price_offset, 
            "scaled_stop_price": scaled_stop_price,
            "good_thru_date": GOOD_THRU_DATE
            }
    
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = request_details)
    
            
        assert server_msg.order_statuses[-1].order.order_type == OrderType.ORDER_TYPE_STL
        assert server_msg.order_statuses[-1].order.duration == Duration.DURATION_GTD
        assert server_msg.order_statuses[-1].order.side == Side.SIDE_SELL
        
    def run_all(self, 
                scaled_limit_price: int, 
                scaled_stop_price: int) -> None:

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

    def modify_order_qty(self, order_id: int, 
                         new_qty: int) -> None:
        modify_request_details = {
            "order_id": order_id,
            "cl_order_id": random_string(length=10),
            "orig_cl_order_id": self.orig_cl_order_id,
            "qty": new_qty
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.MODIFY_ORDER, 
                                  request_details = modify_request_details)

        assert server_msg.order_statuses[-1].status == OrderStatus.FILLED
    
    def modify_order_LMT_price(self, order_id: int, 
                               new_LMT_price: int) -> None:
        modify_request_details = {
            "order_id": order_id,
            "cl_order_id": random_string(length=10),
            "orig_cl_order_id": self.orig_cl_order_id,
            "scaled_limit_price": new_LMT_price
            }

        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.MODIFY_ORDER, 
                                  request_details = modify_request_details)

        assert server_msg.order_statuses[-1].status == OrderStatus.FILLED

    def modify_order_STP_price(self, order_id: int, 
                               new_STP_price: int) -> None:
        modify_request_details = {
            "order_id": order_id,
            "cl_order_id": random_string(length=10),
            "orig_cl_order_id": self.orig_cl_order_id,
            "scaled_stop_price": new_STP_price
            }

        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.MODIFY_ORDER, 
                                  request_details = modify_request_details)

        assert server_msg.order_statuses[-1].status == OrderStatus.FILLED

    def run_all(self, 
                old_LMT_price: int, 
                old_STP_price: int,
                new_LMT_price: int, 
                new_STP_price: int, 
                old_qty: int,
                new_qty: int) -> None:
        # send_once a new order first
        initial_request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_GTC, 
            "side": Side.SIDE_BUY,
            "qty_significant": old_qty, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": old_LMT_price,
            "scaled_stop_price": old_STP_price
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details)
        
        ORDER_ID = server_msg.order_statuses[0].order_id
        self.orig_cl_order_id = initial_request_details["cl_order_id"]
        # Modify this order
        # self.modify_order_qty(ORDER_ID, new_qty) <-Some issue with modify qty 
        self.modify_order_LMT_price(ORDER_ID, new_LMT_price)
        self.modify_order_STP_price(ORDER_ID, new_STP_price)

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
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.CANCEL_ORDER, 
                                  request_details = cancel_request_details)

        assert server_msg.order_statuses[-1].status == OrderStatus.FILLED
        
    def run_all(self, scaled_limit_price: int) -> None:
        # send_once a new order first
        initial_request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_BUY,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price
            }
        
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details)
        
        ORDER_ID = server_msg.order_statuses[0].order_id
        self.orig_cl_order_id = initial_request_details['cl_order_id']

        # Cancel this order
        self.cancel_order(ORDER_ID)
        
class ActivateOrderCases(object):
    """
    Activate order test cases
    """
    def __init__(self, 
                 connect: ConnectCQG,
                 account_id: int,
                 symbol_name: str):
        self.connect = connect
        self.account_id = account_id
        self.symbol_name = symbol_name
        self.orig_cl_order_id = ""
        
    def activate_order(self, order_id: int)->None:
        activate_request_details = {
            "order_id": order_id, 
            "orig_cl_order_id": self.orig_cl_order_id,
            "cl_order_id": random_string(length=10),
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.ACRIVATE_ORDER, 
                                  request_details = activate_request_details)

        assert server_msg.order_statuses[-1].status == OrderStatus.FILLED
 
    
    def run_all(self):
        # send_once a new order first
        initial_request_details = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "suspend": True
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = initial_request_details['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details)

        assert server_msg.order_statuses[0].status == OrderStatus.SUSPENDED
        ORDER_ID = server_msg.order_statuses[0].order_id
        self.orig_cl_order_id = initial_request_details['cl_order_id']

        # Activate this order
        self.activate_order(ORDER_ID)

class GoFlatOrderCases(object):
    """
    Go Flat order test cases
    """

    def __init__(self, 
                 connect: ConnectCQG,
                 account_id: int,
                 symbol_name: str):
        self.connect = connect
        self.account_id = account_id
        self.symbol_name = symbol_name
        self.orig_cl_order_id = ""
        
    def goflat_order(self):
        activate_request_details = {
            "orig_cl_order_id": self.orig_cl_order_id,
            "cl_order_id": random_string(length=10),
            }
        CLOrder = LiveOrderCQG(self.connect, 
                               symbol_name = self.symbol_name, 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg = CLOrder.send_once(request_type=RequestType.GOFLAT_ORDER, 
                                  request_details = activate_request_details)

        assert type(server_msg) == GoFlatStatus
    
    def run_all(self, scaled_limit_price: int):
        # send_once a new MKT order
        initial_request_details_1 = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_MKT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            }
        
        CLOrder_1 = LiveOrderCQG(self.connect, 
                               symbol_name = initial_request_details_1['symbol_name'], 
                               request_id = int(random_string(length=10)), 
                               account_id = self.account_id)
        server_msg_1 = CLOrder_1.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details_1)
        
        # send_once a new LMT order
        initial_request_details_2 = {
            "symbol_name": self.symbol_name,
            "cl_order_id": random_string(length=10),
            "order_type": OrderType.ORDER_TYPE_LMT,
            "duration": Duration.DURATION_DAY, 
            "side": Side.SIDE_SELL,
            "qty_significant": 1, # make sure qty are in Decimal (int) not float
            "qty_exponent": 0, 
            "is_manual": False,
            "scaled_limit_price": scaled_limit_price
            }
        
        CLOrder_2 = LiveOrderCQG(self.connect, 
                                symbol_name = initial_request_details_2['symbol_name'], 
                                request_id = int(random_string(length=10)), 
                                account_id = self.account_id)
        server_msg_2 = CLOrder_2.send_once(request_type=RequestType.NEW_ORDER, 
                                  request_details = initial_request_details_2)
        
        # send_once GoFlat Order, check if there are any remaining orders left
        self.goflat_order()
