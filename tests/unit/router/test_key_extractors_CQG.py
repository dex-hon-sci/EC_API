#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 21:26:23 2026

@author: dexter
"""

from EC_API.protocol.cqg.key_extractors import _extractors
from EC_API.protocol.cqg.router_util import server_msg_type, extract_router_key
from tests.unit.fixtures.server_msg_builders_CQG import *


def test_sever_msg_type() -> None:
    all_msg = build_all_server_msgs()
    for key, msg in all_msg.items():
        top_msg_type = key.split(':')[0]
        out = server_msg_type(msg)[0]
        print(server_msg_type(msg))
        assert out == top_msg_type
        
        
def test_complete_registry() -> None:
   required_extractor_families = [
       'session',  'info', 'rpc', 'sub', 'substream'
       ]
   
   keys = list(_extractors.keys())
   for key in keys:
       assert key in required_extractor_families
    
# Test extraction for sessions
def test_extract_key_logon_result() -> None:
    msg = build_logon_result_server_msg()
    router_key = extract_router_key(msg)
    assert router_key == ('session', 'logon_result', 'single', 0)
    
def test_extract_key_restore_or_join_session_result() -> None:
    msg = build_restore_or_join_session_result_server_msg()
    router_key = extract_router_key(msg)
    assert router_key == ('session', 'restore_or_join_session_result', 'single', 0)

def test_extract_key_concurrent_connection_join_results() -> None:
    msg = build_concurrent_connection_join_results_server_msg
    router_key = extract_router_key(msg)
    assert router_key == ('session', 'concurrent_connection_join_results', 'single', 0)

def test_extract_key_logged_off() -> None:
    msg = build_logged_off_server_msg()
    router_key = extract_router_key(msg)
    assert router_key == ('session', 'logged_off', 'single', 0)

def test_extract_key_pong() -> None:
    msg = build_pong_server_msg()
    router_key = extract_router_key(msg)
    assert router_key == ('session', 'pong', 'single', 0)

def test_extract_key_info_symbol_resolution_report() -> None:...

def test_extract_key_info_session_information_report() -> None:...

def test_extract_key_info_historical_orders_report() -> None:...

def test_extract_key_info_option_maturity_list_report() -> None:...
def test_extract_key_info_instrument_group_report() -> None:...
def test_extract_key_info_at_the_money_strike_report() -> None:...

def test_extract_key_order_request_rejects() -> None:...
def test_extract_key_order_request_acks() -> None:...
def test_extract_key_trade_subscription_statuses() -> None:...
def test_extract_key_trade_snapshot_completions() -> None:...
def test_extract_key_order_statuses() -> None:...
def test_extract_key_position_statuses() -> None:...
def test_extract_key_account_summary_statuses() -> None:...
def test_extract_key_go_flat_statuses() -> None:...

def test_extract_key_market_data_subscription_statuses() -> None:...
def test_extract_key_real_time_market_data() -> None:...

def test_extract_key_time_and_sales_reports() -> None:...
def test_extract_key_time_bar_reports() -> None:...
def test_extract_key_volume_profile_reports() -> None:...
def test_extract_key_non_timed_bar_reports() -> None:...


       
