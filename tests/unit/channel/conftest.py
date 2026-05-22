import pytest
import subprocess
import time
import redis.asyncio as aioredis

@pytest.fixture(scope="session", autouse=True)
def redis_server():
    proc = subprocess.Popen(["redis-server", "--port", "16379"])
    time.sleep(0.5)  # wait for startup
    yield
    proc.terminate()
    proc.wait()
    
@pytest.fixture
async def redis_client():
    client = aioredis.Redis.from_url("redis://localhost:16379", socket_connect_timeout=2)
    await client.flushdb()
    yield client
    await client.flushdb()
    await client.aclose()