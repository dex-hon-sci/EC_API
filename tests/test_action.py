#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 18:38:26 2025

@author: dexter
"""
# In the Future we need a Strategy scanner machine that check compliance of 
# a strategy, for example, scan if the strategy action tree ultimately 
# have an equal qty of Buy/Sell orders (balance check).

from EC_API.op_strategy.action import ActionNode
# Define trigger conditions
def takeprofit_cond():
    return 

def targetentry_cond():
    return

def modifyorder_cond():
    return

def overtime_cond():
    return 

# Define Payloads

# Define Action Nodes
entry_action = ActionNode([],
                          trigger_cond= targetentry_cond,
                          on_filled=None,
                          on_failed=None,
                          on_overtime=None)

takeprofit_action = ActionNode([],
                          trigger_cond= targetentry_cond,
                          on_filled=None,
                          on_failed=None,
                          on_overtime=None)
modify_action = ActionNode([],
                          trigger_cond= modifyorder_cond,
                          on_filled=None,
                          on_failed=None,
                          on_overtime=None)


# Define Action Tree

# Define OpSignal

# Define OpStrategy