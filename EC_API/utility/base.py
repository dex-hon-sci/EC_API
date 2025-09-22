#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 09:44:04 2025

@author: dexter
"""
import random
import time
import pickle
from typing import Callable

def random_string(length: int=16) -> str:
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


def time_it(func: Callable) -> Callable:
    # simple timing function
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()-t1
        print(f"{func.__name__!r} ran in {t2:.4f} seconds.")
        return result
    return wrapper

def save_csv(savefilename: str, save_or_not: bool = True) -> Callable:
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if save_or_not:
                data.to_csv(savefilename, index=False)
                return data
            elif not save_or_not:
                return data
        return wrapper
    return decorator
         
def pickle_save(savefilename: str, save_or_not: bool = True) -> Callable:
    file = open(savefilename, 'wb')
    def decorator(func):
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            if save_or_not:
                pickle.dump(data, file)
                return data
            elif not save_or_not:
                return data
        return wrapper
    return decorator
         
def load_pkl(filename: str): # test function
    output = open(filename, 'rb')
    my_pkl = pickle.load(output)
    print("File:{} is loaded.".format(filename))
    output.close()
    return my_pkl