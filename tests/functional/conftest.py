import aiohttp
import pytest
import json
import asyncio

from typing import List

from aiohttp.client import ClientSession
from elasticsearch import AsyncElasticsearch


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='127.0.0.1:9200') # TODO сделать привязку к переменной окружения
    yield client
    await client.close()


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    #TODO доработать очистку индекса перед новой записью
    async def inner(data: List[dict]):
        bulk_query = get_query_data(data)
        str_query = '\n'.join(bulk_query) + '\n'

        response = await es_client.bulk(str_query, refresh=True)

        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


def get_query_data(data: List[dict]):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index':{'_index':row['index'], 
            '_id':str(row['id'])}}),
            json.dumps(row)
        ])
    return bulk_query


@pytest.fixture
def make_get_request(aio_client:ClientSession):
    async def inner(url, query_data):
        resp_dict = dict()
        async with aio_client.get(url, params=query_data) as response:
            resp_dict['body'] = await response.json()
            resp_dict['headers'] = response.headers
            resp_dict['status'] = response.status
        return resp_dict
    return inner


@pytest.fixture(scope='session')
async def aio_client():
    client = aiohttp.ClientSession()
    yield client
    await client.close()
