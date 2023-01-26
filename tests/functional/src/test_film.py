import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.settings import settings

@pytest.mark.asyncio
async def test_search():
    es_data = [{
        'id': str(uuid.uuid4()),
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
    } for _ in range(60)]

    bulk_query = []
    for row in es_data:
        bulk_query.extend([
            json.dumps({'index': {'_index': 'movies', '_id': row['id']}}),
            json.dumps(row)
        ])

    str_query = '\n'.join(bulk_query) + '\n'

    es_client = AsyncElasticsearch(hosts='http://127.0.0.1:9200/',
                                   validate_cert=False,
                                   use_ssl=False)
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response['errors']:
        raise Exception('Ошибка записи данных в Elasticsearch')

    session = aiohttp.ClientSession()
    url = 'http://localhost:8082/api/v1/films/'
    query_data = {'search': 'The Star'}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        headers = response.headers
        status = response.status
    await session.close()

    assert status == 200
    assert len(body) == 50
