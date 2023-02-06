import pytest


def genre_list():
    return [
        {
            "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
            "name": "Western",
            "popular": 0,
            "description": None,
            "modified": "2023-01-01T00:00:00.309836+00:00",
        },
        {
            "id": "c020dab2-e9bd-4758-95ca-dbe363462173",
            "name": "War",
            "popular": 0,
            "description": "War films description",
            "modified": "2023-01-01T00:00:00.309836+00:00",
        },
    ]


@pytest.fixture
def genre_expected():
    return {
        "id": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
        "name": "Western",
        "popular": 0,
        "description": None,
    }


@pytest.fixture
def genre_list_expected():
    return [
        {
            "uuid": "0b105f87-e0a5-45dc-8ce7-f8632088f390",
            "name": "Western",
            "description": None,
        },
        {
            "uuid": "c020dab2-e9bd-4758-95ca-dbe363462173",
            "name": "War",
            "description": None,
        },
    ]