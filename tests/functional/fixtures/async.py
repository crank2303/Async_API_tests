import aiohttp
import pytest
import asyncio
from aiohttp.client import ClientSession


@pytest.fixture(scope='session')
async def aio_client() -> ClientSession:
    client = aiohttp.ClientSession()
    yield client
    await client.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def make_get_request(aio_client: ClientSession):
    async def inner(url, query_data):
        resp_dict = dict()
        async with aio_client.get(url, params=query_data) as response:
            resp_dict['body'] = await response.json()
            resp_dict['headers'] = response.headers
            resp_dict['status'] = response.status
        return resp_dict
    return inner
