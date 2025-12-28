#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 00:24:56 2025

@author: dexter
"""

from enum import Enum, auto


class MktDataSubLevel(Enum):
    LEVEL_NONE = auto()
    LEVEL_TRADES = auto()
    LEVEL_TRADES_BBA = auto()
    LEVEL_TRADES_BBA_VOLUMES = auto()
    LEVEL_TRADES_BBA_DOM = auto()
    
# =============================================================================
#   enum Level
#   {
#     // Unsubscribe.
#     LEVEL_NONE = 0;
# 
#     // Get only settlement quotes.
#     // NOTE: MarketValues will contain only settlements.
#     LEVEL_SETTLEMENTS = 5;
# 
#     // Get only market values.
#     // Supported only for contracts with filled field ContractMetadata::end_of_day_delay.
#     // NOTE: Array of quotes, requests for quotation, corrections, detailed DOM,
#     // market state in RealTimeMarketData message will be always empty.
#     // NOTE: If current trading day is not yet available (see commentary to field 'end_of_day_delay' in message
#     // ContractMetadata), then MarketValues for today are provided the same way as if trading day was just started:
#     // only required fields and yesterday prices are filled.
#     LEVEL_END_OF_DAY = 6;
# 
#     // Get trade and settlement with volumes (if volumes are known).
#     LEVEL_TRADES = 1;
# 
#     // Get trades and settlements with volumes (if volumes are known), best asks and best bids without volumes.
#     LEVEL_TRADES_BBA = 2;
# 
#     // Get trades, settlements, best asks and best bids with volumes (if volumes are known).
#     LEVEL_TRADES_BBA_VOLUMES = 3;
# 
#     // All price data including DOM (Implied and/or Combined, depending on dom_subscription_type
#     // and MarketDataSubscriptionStatus.actual_dom_subscription_type).
#     LEVEL_TRADES_BBA_DOM = 4;
# 
#     // LEVEL_TRADES_BBA_DOM + Order Details.
#     // Note: Includes information for all orders (both implied and outright).
#     LEVEL_TRADES_BBA_DETAILED_DOM = 7;
#   }
#   enum DomType
#   {
#     // Real-time data shall contain Combined DOM only: a sum of Outright DOM and Implied DOM.
#     // Implied DOM is based on spread orders, Outright DOM is based on outright orders.
#     DOM_TYPE_COMBINED = 0;
# 
#     // Real-time data shall contain only Implied DOM.
#     DOM_TYPE_IMPLIED = 1;
# 
#     // Real-time data shall contain both Combined and Implied DOM.
#     DOM_TYPE_IMPLIED_AND_COMBINED = 2;
#   }
# =============================================================================
