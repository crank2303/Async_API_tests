from http import HTTPStatus

import pytest

from tests.functional.settings import settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search_by_title': 'The Star'},
            {'status': HTTPStatus.OK, 'length': 5}
        ),
        (
            {'search_by_title': 'Mashed patato'},
            {'status': HTTPStatus.OK, 'length': 0}
        ),
        (
            {'search_by_title': 'The Star', 'page[size]': 2},
            {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
            {'search_by_title': 'The Star', 'page[size]': 2, 'page[number]': 3},
            {'status': HTTPStatus.OK, 'length': 1}
        )
    ]
)
@pytest.mark.asyncio
async def test_search_films(make_get_request, query_data, expected_answer):
    url = settings.SERVICE_URL + '/api/v1/films/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search_by_title': 'Ann'},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
        (
            {'search_by_title': 'Mashed patato'},
            {'status': HTTPStatus.OK, 'length': 0}
        ),
        (
            {'search_by_title': 'ruz', 'page[size]': 2},
            {'status': HTTPStatus.OK, 'length': 2}
        ),
        (
            {'search_by_title': 'ruz', 'page[size]': 1, 'page[number]': 2},
            {'status': HTTPStatus.OK, 'length': 1}
        ),
    ]
)
@pytest.mark.asyncio
async def test_search_persons(make_get_request, query_data, expected_answer):
    url = settings.SERVICE_URL + '/api/v1/persons/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']
