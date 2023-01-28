import datetime
import uuid
import json
from typing import List
import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch
from tests.functional.conftest import es_write_data

from tests.functional.settings import settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[size]': '30'},
                {'status': 200, 'length': 30}
        ),
        (
                {'page[size]': '50'},
                {'status': 200, 'length': 50}
        )
    ]
)

@pytest.mark.asyncio
async def test_films_list(es_write_data, make_get_request, es_data: List[dict], query_data, expected_answer):
    await es_write_data(es_data)
    response = await make_get_request('http://localhost:8082/api/v1/films/', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
