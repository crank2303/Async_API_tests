from http import HTTPStatus

import pytest

from tests.functional.settings import settings
from tests.functional.testdata.genres import (genre_expected, genre_list_expected)


@pytest.mark.asyncio
async def test_get_genre_by_id(make_get_request,
                               genre_expected):
    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres/0b105f87-e0a5-45dc-8ce7-f8632088f390',
        {}
    )

    assert response['status'] == HTTPStatus.OK, 'Genre not available by id'
    assert len(response['body']) == len(genre_expected), 'Fields count assert'
    assert response['body'] == genre_expected, 'Data in document assert'


@pytest.mark.asyncio
async def test_get_nonexistent_genre(make_get_request):
    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres/0b105f87-e0a5-45dc-8ce7-f8632088f000',
        {}
    )

    assert response['status'] == HTTPStatus.NOT_FOUND, 'Available nonexistent genre'


@pytest.mark.asyncio
async def test_get_cached_genre(
        make_get_request,
        genre_expected,
        clear_cache,
        es_client
):
    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres/0b105f87-e0a5-45dc-8ce7-f8632088f390',
        {}
    )

    assert response['body'] == genre_expected, 'Check data in document'

    es_response = await es_client.get(
        index='genres',
        id='0b105f87-e0a5-45dc-8ce7-f8632088f000',
        ignore=HTTPStatus.NOT_FOUND
    )

    assert es_response.get('found') is False, \
        'Data in elastic still exists after deletion'
    
    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres/0b105f87-e0a5-45dc-8ce7-f8632088f390',
        {}
    )

    assert response['status'] == HTTPStatus.OK, 'Cache should be available'
    assert response['body'] == genre_expected, 'Incorrect document in cache'


@pytest.mark.asyncio
async def test_full_genre_list(
        make_get_request,
        genre_list_expected
):
    response = await make_get_request(f'{settings.SERVICE_URL}/api/v1/genres',
                                      {'sort': 'popular'})

    assert response['status'] == HTTPStatus.OK, 'Genre list should be available'
    assert len(response['body']) == len(genre_list_expected), \
        'Check genre count'


@pytest.mark.asyncio
async def test_genre_pagination(
        make_get_request,
        genre_list_expected
):
    page_size = min(len(genre_list_expected) - 1, 29)

    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres',
        {'page[size]': page_size,
         'page[number]': 1,
         'sort': 'popular',
         })

    assert response['status'] == HTTPStatus.OK, 'Pagination should be available'
    assert len(response['body']) == page_size, 'Check genre count'

    page_size = len(genre_list_expected) - 1

    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres',
        {'page[size]': page_size,
         'page[number]': 2,
         'sort': 'popular',
         })

    assert len(response['body']) == 1, 'Check genre count'

    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres',
        {'page[size]': -1,
         'sort': 'popular',
         })

    assert response['status'] == HTTPStatus.UNPROCESSABLE_ENTITY

    response = await make_get_request(
        f'{settings.SERVICE_URL}/api/v1/genres',
        {'page[size]': 'a',
         'sort': 'popular',
         })

    assert response['status'] == HTTPStatus.UNPROCESSABLE_ENTITY
