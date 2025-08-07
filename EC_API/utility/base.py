#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 09:44:04 2025

@author: dexter
"""
import random

def random_string(length:int=16):
    """
    Generate a random x-digits alphanumerical string

    Parameters
    ----------
    length : int
        The number of digits.

    Returns
    -------
    Shortcode.

    """
    base = "0123456789"
    
    # Pick a random x (6) digits string from base
    # The amount to (56,800,235,584) possibilities
    code = ''.join([random.choice(base) for i in range(length)])
    return code