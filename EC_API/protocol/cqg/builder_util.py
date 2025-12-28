#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 02:30:44 2025

@author: dexter
"""

from typing import Any, Callable, Mapping, Union, Tuple

_MISSING = object()

def _isnot_null(target_dict: dict[str, Any], key: Any) -> None:
    #print("Check isnot null")
    #for key in list(reference_dict.keys()):
    #    print(key, target_dict.get(key))
    if target_dict.get(key) is None:
        raise KeyError(f"Essential parameter(s): {key} is missing.")
            
# -----------------------------

def _as_types_tuple(t:Union[type, Tuple[type, ...]]) -> tuple[type, ...]:
    return t if isinstance(t, tuple) else (t,)

def _type_name(
    t: Union[type, Tuple[type, ...]]           
    ) -> str:
    ts = _as_types_tuple(t)
    return " | ".join(x.__name__ for x in ts)

def assert_input_types(
    inputs: Mapping[str, Any],
    spec: Mapping[str, tuple[str, Any, Any]]
    ) -> None:
    """
    Ensure all default values conform to the type constraints in spec.
    This prevents silently bad defaults.
    """
    for k, v in inputs.items():
        if k not in spec:
            raise KeyError(f"Default key '{k}' not found in default spec")
        proto_attr, accepted, transform = spec[k]
        
        if v is None:
            continue
        
        if not isinstance(v, _as_types_tuple(accepted)):
            raise TypeError(f"default:{k} must be {_type_name(accepted)}, got {type(v).__name__}")


def apply_optional_fields(
    target: Any, # The Msg
    values: Mapping[str, Any], #
    spec: Mapping[str, tuple[str, tuple[type, ...] | type, Callable[[Any], Any] | None]],
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

        # Transform is for normalization ONLY (e.g. datetime -> epoch_ms)
        if transform is not None:
            v = transform(v)
        print(proto_attr, accepted)
        setattr(target, proto_attr, v)
