import asyncio
import aioredis
import json
from typing import List

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.close()


@pytest.fixture(scope='session', autouse=True)
async def es_delete_index():
    client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                validate_cert=False,
                                use_ssl=False)
    yield client
    await client.indices.delete(index='movies')


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


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


@pytest.fixture(scope='session')
async def redis_client():
    redis = await aioredis.create_redis(f"redis://localhost")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
def clear_cache(redis_client):
    async def inner() -> None:
        await redis_client.flushall(async_op=True)
    return inner


@pytest.fixture
def get_redis(redis_client):
    async def inner(ids):
        value = await redis_client.get(ids)
        return value
    return inner


@pytest.fixture
def es_data_film():
    es_data = [{
        'id': 'a08b62c3-ace0-45ce-9127-57a4b0a70178',
        'imdb_rating': 8.5,
        'mpaa_rating': '12+',
        'genre': [
            {'name': 'Action', 'id': '12'},
            {'name': 'Drama', 'id': '11'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'director': [
            {'id': '185', 'name': 'tom Cruz'}
        ],
        'actors': [
            {'id': '548', 'name': 'Ann'},
            {'id': '974', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '845', 'name': 'Ben'},
            {'id': '564', 'name': 'Howard'}
        ]
    },
        {
            'id': 'a5a6d2dc-1d3f-4324-b848-5df60218d419',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 2',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': 'b26d8dac-eec3-46ff-b19e-20b909b706cc',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 3',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': '7773d331-07b1-41c9-8ba6-1e969c04143a',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 4',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': '9e072978-42b4-4280-b8c8-010b65348ce3',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 5',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        }
    ]
    return es_data

