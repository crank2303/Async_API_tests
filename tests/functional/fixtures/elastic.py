import json
from typing import List

import pytest
from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings
from tests.functional.testdata.genres import genre_list
from tests.functional.testdata.search_persons import get_persons_es_data, get_film_es_data


def get_query_data(_index: str, data: List[dict]):
    bulk_query = []
    for row in data:
        bulk_query.extend([
            json.dumps({'index': {'_index': _index, '_id': str(row['id'])}}),
            json.dumps(row)
        ])
    return bulk_query


async def delete_index(client: AsyncElasticsearch, index: str):
    if await client.indices.exists(index=index):
        await client.indices.delete(index=index)


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{settings.ELASTIC_HOST}:{settings.ELASTIC_PORT}')
    yield client
    indices = ('movies', 'persons', 'genres')
    for index in indices:
        await delete_index(client, index)
    await client.close()


@pytest.fixture
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(_index: str, data: List[dict]):
        bulk_query = get_query_data(_index, data)
        str_query = '\n'.join(bulk_query) + '\n'
        response = await es_client.bulk(str_query, refresh=True)
        if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest.fixture
def es_drop_record(es_client: AsyncElasticsearch):
    async def inner(_index: str, id: str):
        response = await es_client.delete(index=_index, id=id)
        if response['errors']:
            raise Exception('Ошибка удаления данных в Elasticsearch')
    return inner


@pytest.fixture(autouse=True)
async def fill_data(es_write_data):
    index_dict = {
        'movies': get_film_es_data(),
        'persons': get_persons_es_data(),
        'genres': genre_list()
    }
    for _index, data in index_dict.items():
        await es_write_data(_index, data)
