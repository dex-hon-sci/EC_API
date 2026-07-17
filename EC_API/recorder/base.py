from typing import Protocol
from dataclasses import dataclass
class Recorder(Protocol):
    """
    Recorder handles disk-write operations.
    
    We assume the distination is an append-only log.
    
    """
    def __init__(self): pass
    
    async def record(self) -> None: pass

@dataclass(frozen=True)
class SchemaTable:
    """
    A universal standard for injecting schema in the Recorder object.
    """
    def __init__(self, columns: list[tuple[str, str]]):
        self._columns: list[tuple[str, str]] = columns
        
    def create_query(self) -> str: ...
        
    def insert_query(self, db_type: str ="") -> str:...