from http import HTTPStatus

import pytest

from tests.functional.settings import settings


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            {'sort': 'full_name'},
            {'status': HTTPStatus.OK, 'length': 3, 'name': 'tom Cruz'}
        ),
        (
            {'sort': '-full_name'},
            {'status': HTTPStatus.OK, 'length': 3, 'name': 'Ann'}
        ),
        (
            {'page[size]': 2},
            {'status': HTTPStatus.OK, 'length': 2, 'name': 'tom Cruz'}
        ),
        (
            {'page[size]': 1, 'page[number]': 3},
            {'status': HTTPStatus.OK, 'length': 1, 'name': 'Howard Truz'}
        ),
    ]
)
@pytest.mark.asyncio
async def test_persons(make_get_request, query_data, expected_answer):
    url = settings.SERVICE_URL + '/api/v1/persons'

    request = await make_get_request(url, query_data)

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']
    assert request['body'][0]['full_name'] == expected_answer['name']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            'mhfd8dac-eec3-46ff-b19e-20b909b706cc',
            {'status': HTTPStatus.OK, 'length': 5}
        ),
        (
            '1',
            {'status': HTTPStatus.OK, 'length': 0}
        ),
    ]
)
@pytest.mark.asyncio
async def test_persons_uuid(make_get_request, query_data, expected_answer):
    url = settings.SERVICE_URL + '/api/v1/persons/' + query_data

    request = await make_get_request(url, {})

    assert request['status'] == expected_answer['status']
    assert len(request['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
            'mhfd8dac-eec3-46ff-b19e-20b909b706cc',
            {'status': HTTPStatus.OK, 'films_actor': 0, 'films_director': 0, 'films_writer': 3}
        ),
        (
            '9e072978-90b4-4330-b8c8-010b65348ce3',
            {'status': HTTPStatus.OK, 'films_actor': 1, 'films_director': 1, 'films_writer':2}
        ),
    ]
)
@pytest.mark.asyncio
async def test_persons_uuid_film(make_get_request, query_data, expected_answer):
    url = f'{settings.SERVICE_URL}/api/v1/persons/{query_data}/film'

    request = await make_get_request(url, {})

    assert request['status'] == expected_answer['status']
    assert len(request['body'][0]['films_actor']) == expected_answer['films_actor']
    assert len(request['body'][0]['films_director']) == expected_answer['films_director']
    assert len(request['body'][0]['films_writer']) == expected_answer['films_writer']


@pytest.mark.asyncio   
async def test_persons_uuid_film_empty(make_get_request):
    url = f'{settings.SERVICE_URL}/api/v1/persons/1/film'

    request = await make_get_request(url, {})

    assert request['status'] == HTTPStatus.OK
    assert len(request['body']) == 0


@pytest.mark.asyncio
async def test_persons_uuid_cache(make_get_request, es_drop_record):
    url = f'{settings.SERVICE_URL}/api/v1/persons/mhfd8dac-eec3-46ff-b19e-20b909b706cc'
    await make_get_request(url, {})
    es_drop_record('persons', 'mhfd8dac-eec3-46ff-b19e-20b909b706cc')

    request = await make_get_request(url, {})

    assert request['status'] == HTTPStatus.OK
    assert len(request['body']) == 5
