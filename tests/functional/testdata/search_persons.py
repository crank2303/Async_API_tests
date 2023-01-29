import uuid
import pytest
import random


def get_persons_es_data():
    return [{
        "index":'persons',
        "id": str(uuid.uuid4()),
        "full_name": "Mat Lucas",
        "film_ids_director": [str(uuid.uuid4) for film in range(random.randint(0,6))],
        "film_ids_writer": [str(uuid.uuid4) for film in range(random.randint(0,6))],
        "film_ids_actor": [str(uuid.uuid4) for film in range(random.randint(0,6))],
    } for actor in range(60)
    ]

@pytest.fixture
def list_person():
    return [{

        "id": "6dd77305-18ee-4d2e-9215-fd1a496ccfdf",
        "full_name": "Mat Lucas",
        "role": "actor",
        "film_ids": [
        "044beafe-fe25-4edc-95f4-adbb8979c35b",
        "fdfc8266-5ece-4d85-b614-3cfe9be97b71"
        ]
    },
    {
        "_index": "persons",
        "_id": "3eca95e0-2c3d-4fe1-aef6-93a37678b369",
        "id": "3eca95e0-2c3d-4fe1-aef6-93a37678b369",
        "full_name": "Alan Ruck",
        "role": "actor",
        "film_ids": [
        "d2d9b15d-a134-446a-af51-eb8c5207fd46"
        ]
    },
    {
        "_index": "persons",
        "_id": "ae0113af-2b40-4578-a530-060be491d567",
        "id": "ae0113af-2b40-4578-a530-060be491d567",
        "full_name": "Luca Boni",
        "role": "director",
        "film_ids": [
        "2ae92dcc-e043-4a0c-a2cd-6146650b3c71"
        ]
    }]

@pytest.fixture
def person_expected():
    return {
        "id": "ae0113af-2b40-4578-a530-060be491d567",
        "full_name": "Luca Boni",
        "role": "director",
        "film_ids": [
        "2ae92dcc-e043-4a0c-a2cd-6146650b3c71"
        ]
    }

@pytest.fixture
def person_list_expected():
    return 


