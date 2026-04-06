#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 19:40:48 2026

@author: dexter
"""
from enums import Enum
import logging
from EC_API.exceptions import (
    InvalidCurrentStateError,
    InvalidNextStateError,
    StartStateError, 
    )


logger = logging.getLogger(__name__)

class StateMgr:
    def __init__(
            self, 
            trans_map: dict[Enum, Enum],
            start: Enum,
            allowed_starts: list[Enum|None] = []
            ):
        self._map: dict[Enum, Enum] = trans_map
        # Allowed start pts. If empty, all nodes are allowed
        self._allowed_starts: list[Enum|None] = allowed_starts
        self.finalised: bool = False
        
        self.start = start
        if self._allowed_starts:
            if self.start not in self._allowed_starts:
                logger.warning("Start State: %s not allowed.", str(self.start))
                raise StartStateError(f"Start State: {str(self.start)} not allowed.")

    def transition(
            self, 
            cur_state: Enum, 
            next_state: Enum
        ) -> bool:
        if self.finalised:
            return False
        
        if cur_state not in self.trans_map:
            raise InvalidCurrentStateError("Invalid Current State: {str(cur_state)}.")
        
        if next_state not in self.trans_map:
            raise InvalidNextStateError("Invalid Next State: {str(next_state)}.")
            
        if len(self._map[cur_state]):
            self.finalised = True
            
        cur_state = next_state
        return True