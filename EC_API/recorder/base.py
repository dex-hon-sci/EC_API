from typing import Protocol, ClassVar
from dataclasses import dataclass

class Recorder(Protocol):
    """
    Recorder handles disk-write operations.
    
    We assume the distination is an append-only log.
    
    """
    def __init__(self): pass
    async def start(self): pass
    async def stop(self): pass
    async def record(self) -> None: pass

@dataclass(frozen=True)
class SQLSchemaTable:
    """
    A universal standard for injecting schema in the Recorder object.
    
    We expect a SQL-based DB schema here.
    """
    table_name: str
    columns: tuple[tuple[str, str],...]
    
    _ALLOWED_TYPES: ClassVar[frozenset] = frozenset([
        "NULL", "INTEGER", "REAL", "TEXT", "BLOB"
        ])
    _ALLOWED_DB: ClassVar[frozenset] = frozenset([
        "aiosqlite", "sqlite3", "asyncpg", "psycopg", "pymysql", "mysqlclient"
        ])
    
    def __post_init__(self):
        for col_name, col_typ in self.columns:
            if not isinstance(col_name, str): 
                raise TypeError(f"column name: {col_name} must be a str.")
                
            if col_typ not in self._ALLOWED_TYPES:
                raise ValueError(f"column name: {col_name} not in the accepted data type: {col_typ}.")
        
    def create_query(self) -> str:
        cols = ",\n".join(f"{col} {typ}" for col, typ in self.columns)
        return f"CREATE TABLE IF NOT EXISTS {self.table_name} (\n {cols}\n)"
        
    def insert_query(self, db_type: str) -> str:
        col_name = ", ".join([x for x, _ in self.columns])
        match db_type:
            case "aiosqlite" | "sqlite3":
                placeholder = ", ".join(["?" for _ in self.columns]) 
            case "asyncpg":
                placeholder = ", ".join([f"${i+1}" for i, _ in enumerate(self.columns)]) 
            case "psycopg" | "pymysql" | "mysqlclient":
                placeholder = ", ".join(["%s" for _ in self.columns]) 
            case _:
                raise ValueError(f"Invalid db_type: {db_type}. Only the following db are supported: {self._ALLOWED_DB}.")
                
        return f"INSERT INTO {self.table_name} ({col_name}) VALUES ({placeholder})"