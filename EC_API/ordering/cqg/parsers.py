#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 03:05:48 2026

@author: dexter
"""
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg


def parse_order_request_rejects_server_msg(msg:ServerMsg):
    ...
    
def parse_order_request_acks_server_msg(msg:ServerMsg):
    ...

def parse_trade_subscription_statuses_server_msg(msg:ServerMsg):
    ...


def parse_trade_snapshot_completetions_server_msg(msg:ServerMsg):
    
    ...

def parse_order_statuses_server_msg(msg:ServerMsg):
    ...

    
def parse_position_statuses_server_msg(msg:ServerMsg):
    ...

def parse_account_summary_statuses_server_msg(msg:ServerMsg):
    ...

    
def parse_go_flat_statuses_server_msg(msg:ServerMsg):
    ...
