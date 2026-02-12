#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 12:12:27 2025

@author: dexter
"""


# =============================================================================
# Trade Subscriptions Status
# STATUS_CODE_SUCCESS = 0;
# 
# // Currently subscription is [partially] disconnect because of communication issues.
# // NOTE: Clients should not resubscribe in this case, the server will restore subscription with
# // sending SUCCESS status once communication issues are resolved following with all necessary data updates.
# STATUS_CODE_DISCONNECTED = 1;
# 
# // failure codes (100+)
# STATUS_CODE_FAILURE = 101;
# 
# // The limit of the subscriptions has been violated.
# STATUS_CODE_SUBSCRIPTION_LIMIT_VIOLATION = 102;
# 
# // Unknown or ambiguous account, sales series number, or brokerage id in the subscription.
# STATUS_CODE_INVALID_PUBLICATION_ID = 103;
# 
# // The limit of subscribed accounts has been violated.
# STATUS_CODE_SUBSCRIBED_ACCOUNTS_LIMIT_VIOLATION = 104;
# =============================================================================