import numpy as np
import pandas as pd
from pandas import Series, DataFrame as Frame, Index
from typing import *

from typing import Any, Callable
from EC_API.ext.WebAPI.webapi_2_pb2 import ServerMsg

from datetime import datetime, timedelta, tzinfo

# Generic types
Typ = TypeVar("T")
Func = TypeVar("F", bound=Callable[..., Any])

ServerMsgType = TypeVar("T")
# Config

# Arrays
Array = np.ndarray  # ready to be used for n-dim data
Array1D = np.ndarray
Array2D = np.ndarray
Array3D = np.ndarray
Record = np.void
RecordArray = np.ndarray


# --- Routers
# (msg_family, msg_type, id_field_name, id)
RouterKey = tuple[str, str, str, int|str]
type Extractor_func = Callable[ServerMsgType]

# (msg_family, msg_type, is_repeated, is_)
KeyHit = tuple[str, int, bool, bool]

# --- Parsers
type Parser_func = Callable[ServerMsgType]
metadata_parsers: dict[str, Parser_func] = {}

# --- Connect
LogonResultType = dict[str, Any]
LogoffResultType = dict[str, Any]
RestoreResultType = dict[str, Any]
PongType = tuple[str, int, int]
# --- Monitor
# contract_id, O, H, L, C, volume_significand, volume_exponent, volume_significand, correct_price_scale
MarketValueType = tuple[int, int, int, int, int, int, int]

# contract_id, quote_utc_time, type, scaled_price, scaled_source_price
QuotesValueType = tuple[int, int, Any, int, int]

# --- LiveOrder
