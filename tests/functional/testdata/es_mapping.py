import json

from elasticsearch import Elasticsearch
from es_schemas.genre_schema import SCHEMA as GENRES_INDEX_BODY
from es_schemas.filmwork_schema import SCHEMA as FILMWORKS_INDEX_BODY
from es_schemas.person_schema import SCHEMA as PERSONS_INDEX_BODY

INDEXES = {
    "persons": PERSONS_INDEX_BODY,
    "genres": GENRES_INDEX_BODY,
    "movies": FILMWORKS_INDEX_BODY,
}

genres = [
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
        "description": None,
        "modified": "2023-01-01T00:00:00.309836+00:00",
    },
]
persons = [
    {
        "id": "4a416628-4a36-431c-9121-513674dae840",
        "full_name": "Zoe Saldana",
        "role": "actor",
        "film_ids": [
            "6ecc7a32-14a1-4da8-9881-bf81f0f09897",
            "b1f1e8a6-e310-47d9-a93c-6a7b192bac0e"
        ],
        "modified": "2023-01-01T00:00:00.309836+00:00",
    },
    {
        "id": "8a34f121-7ce6-4021-b467-abec993fc6cd",
        "full_name": "Zachary Quinto",
        "role": "actor",
        "film_ids": [
            "020adfa7-7251-4fb9-b6db-07b60664cb67",
            "4af6c9c9-0be0-4864-b1e9-7f87dd59ee1f",
            "6ecc7a32-14a1-4da8-9881-bf81f0f09897",
            "b1f1e8a6-e310-47d9-a93c-6a7b192bac0e"
        ],
        "modified": "2023-01-01T00:00:00.309836+00:00",
    },
]

movies = [
    {
        "id": "2a090dde-f688-46fe-a9f4-b781a985275e",
        "title": "Star Wars: Knights of the Old Republic",
        "imdb_rating": "9.6",
        "modified": "2023-01-01T00:00:00.309836+00:00",
    },
    {
        "id": "c241874f-53d3-411a-8894-37c19d8bf010",
        "title": "Star Wars SC 38 Reimagined",
        "imdb_rating": "9.5",
        "modified": "2023-01-01T00:00:00.309836+00:00",
    },
]


def data_for_elastic() -> str:
    json_list = []
    for record in persons:
        index_info = {"index": {"_index": "persons", "_id": record["id"]}}
        json_list.append(index_info)
        json_list.append(record)
    for record in movies:
        index_info = {"index": {"_index": "movies", "_id": record["id"]}}
        json_list.append(index_info)
        json_list.append(record)
    for record in genres:
        index_info = {"index": {"_index": "genres", "_id": record["id"]}}
        json_list.append(index_info)
        json_list.append(record)

    json_list = "\n".join(json.dumps(j) for j in json_list)
    json_list += "\n"

    return json_list


def main():
    es_client = Elasticsearch(f"localhost:9200")  # TODO Заменить на ос
    for index in INDEXES:
        if not es_client.es.indices.exists(index=index):
            es_client.es.indices.create(index=index, body=INDEXES[index])

    index_data = {"movies": movies, "genres": genres, "persons": persons}
    for index, data in index_data.items():
        for d in data:
            es_client.index(index=index, id=d["id"], body=d, doc_type="_doc")


if __name__ == "__main__":
    main()
