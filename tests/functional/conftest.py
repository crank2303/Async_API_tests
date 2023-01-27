
import pytest
from typing import List
import json
from elasticsearch import AsyncElasticsearch
import aiohttp


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.close()
@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict]):
        bulk_query = []
        for row in data:
            bulk_query.extend([
                json.dumps({'index': {'_index': 'movies', '_id': row['id']}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture(scope='session')
async def aiohttp_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(aiohttp_session):
    async def inner(url, params):
        resp_dict = dict()
        async with aiohttp_session.get(url, params=params) as response:
            resp_dict['body'] = await response.json()
            resp_dict['headers'] = response.headers
            resp_dict['status'] = response.status
        return resp_dict
    return inner
