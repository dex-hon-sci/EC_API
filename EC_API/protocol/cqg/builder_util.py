#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 02:30:44 2025

@author: dexter
"""

from typing import Any, Callable, Mapping

_MISSING = object()

def apply_optional_fields(
    target: Any,
    values: Mapping[str, Any],
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

        if not isinstance(v, accepted if isinstance(accepted, tuple) else (accepted,)):
            raise TypeError(f"{user_key} must be {accepted}, got {type(v)}")

        if transform is not None:
            v = transform(v)

        setattr(target, proto_attr, v)
