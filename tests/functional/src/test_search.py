import datetime
import uuid
import json

import aiohttp
import pytest

from elasticsearch import AsyncElasticsearch

from tests.functional.testdata.search_films import get_films_es_data
from tests.functional.testdata.search_persons import get_persons_es_data
from tests.functional.settings import settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search_by_title': 'The Star'},
            {'status': 200, 'length': 50}
        ),
        (
            {'search_by_title': 'Mashed patato'},
            {'status': 200, 'length': 0}
        ),
        (
            {'search_by_title': 'The Star', 'page[size]': 2},
            {'status': 200, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_films(es_write_data, make_get_request, query_data, expected_answer):
    es_data = get_films_es_data()

    await es_write_data(es_data)

    url = settings.SERVICE_URL + '/api/v1/films/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search_by_title': 'Mat Luc'},#TODO переделать имя поля для поиска + описание + убрать разибите на отдельные роли
            {'status': 200, 'length': 50}
        ),
        (
            {'search_by_title': 'Mashed patato'},
            {'status': 200, 'length': 0}
        ),
        (
            {'search_by_title': 'Mat Lucas', 'page[size]': 2},
            {'status': 200, 'length': 2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(es_write_data, make_get_request, query_data, expected_answer):
    es_data = get_persons_es_data()

    await es_write_data(es_data)

    url = settings.SERVICE_URL + '/api/v1/persons/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']