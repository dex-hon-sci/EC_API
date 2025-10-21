#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 15:46:18 2025

@author: dexter
"""
from pathlib import Path

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, Enum as SqlEnum
from sqlalchemy import DateTime
from sqlalchemy.types import PickleType
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# EC Trade System import
from EC_API.payload.enums import PayloadStatus
from EC_API.ordering.enums import RequestType


#BASE_DIR = Path(__file__).resolve().parent
BASE_DIR = "/home/dexter/Euler_Capital_codes/EC_API/tests/test_orders.db"
DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}"
engine = create_async_engine(DATABASE_URL, echo=False)
Base = declarative_base()

TEST_ASYNC_SESSION = async_sessionmaker(engine, expire_on_commit=False)

print("DATABASE_URL", DATABASE_URL)
class BaseTable(Base):
    __abstract__ = True  

    request_id = Column(Integer, primary_key=True)
    account_id = Column(Integer)
    status = Column(SqlEnum(PayloadStatus), nullable=False)
    order_request_type = Column(SqlEnum(RequestType), nullable=False)
    start_time = Column(DateTime, nullable=False) # Effective time
    end_time = Column(DateTime, nullable=False) # Expiration time
    order_info = Column(PickleType, nullable=True)
    
class TestStorage(BaseTable):
    __tablename__ = "Test_Storage"
    
    def __repr__(self):
        return f"<Test_Storage(id={self.request_id}, status={self.status}, type={self.order_request_type}, order_info = {self.order_info})>"


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
