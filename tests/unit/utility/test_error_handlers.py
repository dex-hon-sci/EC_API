#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:26:47 2026

@author: dexter
"""

from EC_API.utility.error_handlers import msg_io_error_handler
from EC_API.exceptions import (
    MsgBuilderError, TradeSessionTimeOutError
    )


def test_msg_io_error_handler_valid() -> None:
    
    msg_io_error_handler(MsgBuilderError, TradeSessionTimeOutError)