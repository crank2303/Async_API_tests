import pytest


@pytest.mark.asyncio  # Тест на проверку списка фильмов
async def test_films_list(make_get_request):
    response = await make_get_request('http://localhost:8082/api/v1/films/', None)
    assert response['status'] == 200
    assert len(response['body']) == 5


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'page[size]': '4', 'page[number]': '1'},
                {'status': 200, 'length': 4}
        ),
        (
                {'page[size]': '3', 'page[number]': '2'},
                {'status': 200, 'length': 2}
        )
    ]
)
@pytest.mark.asyncio  # 2 теста на проверку пагинации (количество элементов на странице и номер страницы)
async def test_films_list_page(make_get_request, query_data, expected_answer):
    response = await make_get_request('http://localhost:8082/api/v1/films/', query_data)
    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.asyncio  # тест на существующий фильм
async def test_film_exist(make_get_request):
    response = await make_get_request('http://localhost:8082/api/v1/films/a08b62c3-ace0-45ce-9127-57a4b0a70178', None)
    assert response['status'] == 200
    assert response['body']['title'] == 'The Star'


@pytest.mark.asyncio  # тест на несуществующий фильм
async def test_film_not_exist(make_get_request):
    response = await make_get_request('http://localhost:8082/api/v1/films/a08b62c3-ace0-45ce-9127-57a4b0a70179', None)
    assert response['status'] == 404


@pytest.mark.asyncio  # тест на кеш
async def test_film_cache(make_get_request, clear_cache, get_redis):
    await clear_cache()
    value_before_cache = await get_redis('e072978-42b4-4280-b8c8-010b65348ce3')
    assert value_before_cache == None
    await make_get_request('http://localhost:8082/api/v1/films/9e072978-42b4-4280-b8c8-010b65348ce3', None)
    value_after_cache = await get_redis('movies:film_id:9e072978-42b4-4280-b8c8-010b65348ce3')
    assert value_after_cache != None