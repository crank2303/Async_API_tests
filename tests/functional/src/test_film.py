from http import HTTPStatus

import pytest

from tests.functional.settings import settings


@pytest.mark.asyncio
async def test_films_list(make_get_request):
    response = await make_get_request(f'{settings.SERVICE_URL}/api/v1/films/', None)
    assert response['status'] == HTTPStatus.OK
    assert len(response['body']) == 5


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[size]': '4', 'page[number]': '1'},
                {'status': HTTPStatus.OK, 'length': 4}
        ),
        (
                {'page[size]': '3', 'page[number]': '2'},
                {'status': HTTPStatus.OK, 'length': 2}
        )
    ]
)
@pytest.mark.asyncio
async def test_films_list_page(make_get_request, query_data, expected_answer):
    response = await make_get_request(f'{settings.SERVICE_URL}/api/v1/films/', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio
async def test_film_exist(make_get_request):
    response = await make_get_request(f'{settings.SERVICE_URL}/api/v1/films/a08b62c3-ace0-45ce-9127-57a4b0a70178', None)
    assert response['status'] == HTTPStatus.OK
    assert response['body']['title'] == 'The Star'


@pytest.mark.asyncio
async def test_film_not_exist(make_get_request):
    response = await make_get_request(f'{settings.SERVICE_URL}/api/v1/films/a08b62c3-ace0-45ce-9127-57a4b0a70179', None)
    assert response['status'] == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_film_cache(make_get_request, clear_cache, get_redis):
    await clear_cache()
    value_before_cache = await get_redis('e072978-42b4-4280-b8c8-010b65348ce3')
    assert value_before_cache is None

    await make_get_request(f'{settings.SERVICE_URL}/api/v1/films/9e072978-42b4-4280-b8c8-010b65348ce3', None)
    value_after_cache = await get_redis('movies:film_id:9e072978-42b4-4280-b8c8-010b65348ce3')
    assert value_after_cache is not None
