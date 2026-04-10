#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:13:49 2026

@author: dexter
"""
import asyncio
from contextlib import contextmanager
from EC_API.exceptions import EC_APIError, MsgBuilderError, MsgParserError

@contextmanager
def msg_io_error_handler(
        output_error: EC_APIError,
        timeout_error: EC_APIError = Exception,
        ) -> EC_APIError:
    try:
        yield
    except (MsgBuilderError, MsgParserError) as e:
        raise output_error(str(e)) from e
    except asyncio.TimeoutError as e:
        raise timeout_error(str(e)) from e