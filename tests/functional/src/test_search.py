import pytest

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
async def test_search_films(make_get_request, query_data, expected_answer):

    url = settings.SERVICE_URL + '/api/v1/films/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'search_by_title': 'Anna'},
            {'status': 200, 'length': 1}
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
async def test_search_persons(make_get_request, query_data, expected_answer):

    url = settings.SERVICE_URL + '/api/v1/persons/search'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']