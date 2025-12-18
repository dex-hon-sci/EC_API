#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 02:30:44 2025

@author: dexter
"""

from typing import Any, Callable, Mapping, Union, Tuple

_MISSING = object()

def _as_types_tuple(t:Union[type, Tuple[type, ...]]) -> tuple[type, ...]:
    return t if isinstance(t, tuple) else (t,)

def _type_name(
    t: Union[type, Tuple[type, ...]]           
    ) -> str:
    ts = _as_types_tuple(t)
    return " | ".join(x.__name__ for x in ts)

def _assert_type(
    name: str, value: Any, 
    accepted: Union[type, Tuple[type, ...]]
    ) -> None:
    if not isinstance(value, _as_types_tuple(accepted)):
        raise TypeError(f"{name} must be {_type_name(accepted)}, got {type(value).__name__}")

def assert_defaults_types(
    defaults: Mapping[str, Any],
    spec: Mapping[str, tuple[str, Any, Any]]
    ) -> None:
    """
    Ensure all default values conform to the type constraints in spec.
    This prevents silently bad defaults.
    """
    for k, v in defaults.items():
        if k not in spec:
            raise KeyError(f"Default key '{k}' not found in optional spec")
        proto_attr, accepted, transform = spec[k]
        if v is None:
            continue
        _assert_type(f"default:{k}", v, accepted)
        # Optional: also validate transform doesn't explode at import time.
        # But DON'T apply transform here; just check type of input.


def apply_optional_fields(
    target: Any, # The Msg
    values: Mapping[str, Any], #
    spec: Mapping[str, tuple[str, tuple[type, ...] | type, Callable[[Any], Any] | None]],
    *,
    strict: bool = True,
    ) -> None:
    """
    target: protobuf message object to mutate
    values: kwargs from caller (your builder input)
    spec: map of user_key -> (proto_attr_name, accepted_types, transform_fn?)

    strict=True: raise if caller provides unknown optional keys
    """
    if strict:
        unknown = set(values.keys()) - set(spec.keys())
        if unknown:
            raise TypeError(f"Unknown optional fields: {sorted(unknown)}")

    for user_key, (proto_attr, accepted, transform) in spec.items():
        v = values.get(user_key, _MISSING)
        if v is _MISSING or v is None:
            continue

        # Type-check caller value (prevents bool("BullShit") etc.)
        _assert_type(user_key, v, accepted)

        # Transform is for normalization ONLY (e.g. datetime -> epoch_ms)
        if transform is not None:
            v = transform(v)

        setattr(target, proto_attr, v)
