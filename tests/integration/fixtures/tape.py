#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:29:58 2026

@author: dexter
"""
from typing import Protocol, Iterator

class SourceTape(Protocol):
    def replay(self) -> Iterator[int]: ...


class GBMTape:
    def __init__(self, seed: int):
        self._seed = seed
        
    def replay(self):...