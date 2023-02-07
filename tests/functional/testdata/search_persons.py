def get_persons_es_data():
    es_data = [{
        "index": 'persons',
        "id": 'a08b62c3-a9e0-45ce-9127-574b0xa70178',
        "full_name": "tom Cruz",
        "film_ids_director": [
                    'a08b62c3-ace0-45ce-9127-57a4b0a70178',
                    'a5a6d2dc-1d3f-4324-b848-5df60218d419',
                    'b26d8dac-eec3-46ff-b19e-20b909b706cc',
                    '7773d331-07b1-41c9-8ba6-1e969c04143a',
                    '9e072978-42b4-4280-b8c8-010b65348ce3',
        ],
        "film_ids_writer": [],
        "film_ids_actor": [],
    },
        {
        "index": 'persons',
        "id": 'mhfd8dac-eec3-46ff-b19e-20b909b706cc',
        "full_name": "Ann",
        "film_ids_director": [],
        "film_ids_writer": [
                    'a08b62c3-ace0-45ce-9127-57a4b0a70178',
                    'a5a6d2dc-1d3f-4324-b848-5df60218d419',
                    'b26d8dac-eec3-46ff-b19e-20b909b706cc',

        ],
        "film_ids_actor": [],
    },
        {
        "index": 'persons',
        "id": '9e072978-90b4-4330-b8c8-010b65348ce3',
        "full_name": "Howard Truz",
        "film_ids_director": ['a08b62c3-ace0-45ce-9127-57a4b0a70178',
                              ],
        "film_ids_writer": [
                    'a5a6d2dc-1d3f-4324-b848-5df60218d419',
                    'b26d8dac-eec3-46ff-b19e-20b909b706cc',
                    ],
        "film_ids_actor": ['9e072978-42b4-4280-b8c8-010b65348ce3',
                           ],
    },
    ]
    return es_data


def get_film_es_data():
    es_data = [{
        'id': 'a08b62c3-ace0-45ce-9127-57a4b0a70178',
        'imdb_rating': 8.5,
        'mpaa_rating': '12+',
        'genre': [
            {'name': 'Action', 'id': '12'},
            {'name': 'Drama', 'id': '11'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'director': [
            {'id': '185', 'name': 'tom Cruz'}
        ],
        'actors': [
            {'id': '548', 'name': 'Ann'},
            {'id': '974', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '845', 'name': 'Ben'},
            {'id': '564', 'name': 'Howard'}
        ]
    },
        {
            'id': 'a5a6d2dc-1d3f-4324-b848-5df60218d419',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 2',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': 'b26d8dac-eec3-46ff-b19e-20b909b706cc',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 3',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': '7773d331-07b1-41c9-8ba6-1e969c04143a',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 4',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        },
        {
            'id': '9e072978-42b4-4280-b8c8-010b65348ce3',
            'imdb_rating': 8.5,
            'mpaa_rating': '12+',
            'genre': [
                {'name': 'Action', 'id': '12'},
                {'name': 'Drama', 'id': '11'}
            ],
            'title': 'The Star 5',
            'description': 'New World',
            'director': [
                {'id': '185', 'name': 'tom Cruz'}
            ],
            'actors': [
                {'id': '548', 'name': 'Ann'},
                {'id': '974', 'name': 'Bob'}
            ],
            'writers': [
                {'id': '845', 'name': 'Ben'},
                {'id': '564', 'name': 'Howard'}
            ]
        }
    ]
    return es_data
