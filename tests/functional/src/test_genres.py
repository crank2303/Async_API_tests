import pytest

from testdata.genres import (genre_expected,
                             genre_list, genre_list_expected)


@pytest.mark.asyncio
async def test_get_genre_by_id(send_data_to_elastic,
                               genre_list,
                               make_get_request,
                               genre_expected):
    async with send_data_to_elastic(data=genre_list):
        response = await make_get_request(
            '/genre/0b105f87-e0a5-45dc-8ce7-f8632088f390'
        )

        assert response.status == 200, 'Genre not available by id'
        assert len(response.body) == len(genre_expected), 'Fields count assert'
        assert response.body == genre_expected, 'Data in document assert'
