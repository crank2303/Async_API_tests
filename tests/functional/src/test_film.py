import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch
from tests.functional.conftest import es_write_data

from tests.functional.settings import settings




@pytest.mark.asyncio
async def test_films(es_write_data, make_get_request):
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

    await es_write_data(es_data)

    response = await make_get_request('http://localhost:8082/api/v1/films/', None)

    assert response['status'] == 200
    assert len(response['body']) == 50
