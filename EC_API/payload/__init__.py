#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:26:23 2025

@author: dexter

The payload module manage and check the prerequisites (Historical Data) before
sending the payload package through the ordering function to send out liveorder.

It should be independent of WebAPI provider.

Signal.actions -> CQGLiveOrder -> Payload


"""
from EC_API.payload.enums import PayloadStatus
from EC_API.payload.base import Payload, ExecutePayload_CQG

__all__ = [
    "Payload",
    "ExecutePayload_CQG",
    "PayloadStatus",
    ]
__pdoc__ = {k: False for k in __all__}