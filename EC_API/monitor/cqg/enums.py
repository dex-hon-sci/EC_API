#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 00:23:11 2025

@author: dexter
"""
from enum import Enum, auto

from EC_API.ext.WebAPI.market_data_2_pb2 import MarketDataSubscription as CQG_MDS
from EC_API.monitor.enums import MktDataSubLevel
from EC_API.monitor.cqg.enums import MktDataSubLevelCQG


class MktDataSubLevelCQG(Enum):
    LEVEL_SETTLEMENTS = auto()
    LEVEL_TRADES_BBA_DETAILED_DOM = auto()
    LEVEL_END_OF_DAY = auto()

MKTDATASUBLEVEL_MAP_INT2CQG = {
    MktDataSubLevel.LEVEL_NONE: CQG_MDS.Level.LEVEL_NONE,
    MktDataSubLevel.LEVEL_TRADES: CQG_MDS.Level.LEVEL_TRADES,
    MktDataSubLevel.LEVEL_TRADES_BBA: CQG_MDS.Level.LEVEL_TRADES_BBA,
    MktDataSubLevel.LEVEL_TRADES_BBA_VOLUMES: CQG_MDS.Level.LEVEL_TRADES_BBA_VOLUMES,
    MktDataSubLevel.LEVEL_TRADES_BBA_DOM: CQG_MDS.Level.LEVEL_TRADES_BBA_DOM,
    MktDataSubLevelCQG.LEVEL_SETTLEMENTS: CQG_MDS.Level.LEVEL_SETTLEMENTS,
    MktDataSubLevelCQG.LEVEL_TRADES_BBA_DETAILED_DOM: CQG_MDS.Level.LEVEL_TRADES_BBA_DETAILED_DOM,
    MktDataSubLevelCQG.LEVEL_END_OF_DAY: CQG_MDS.Level.LEVEL_END_OF_DAY
    }