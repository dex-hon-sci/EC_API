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
class SQLSchemaTable:
    """
    A universal standard for injecting schema in the Recorder object.
    
    We expect a SQL-based DB schema here.
    """
    table_name: str
    columns: list[tuple[str, str],...]

    def __post_init__(self, table_name: str, columns: list[tuple[str, str]]):
        
        # Column format CHECK
        ...
    def create_query(self) -> str:
        cols = ", \n".join(f"{col} {typ}" for col, typ in self.columns)
        return f"CREATE TABLE IF NOT EXIST {self.table_name} (\n {cols}\n)"
        
    def insert_query(self, db_type: str ="") -> str:
        
        
        return f"INSERT INTO {self._table_name} ({', '.join({})}) VALUES ({})"