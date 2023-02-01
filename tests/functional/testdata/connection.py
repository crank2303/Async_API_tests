import aiohttp
import json

from elasticsearch import Elasticsearch

from search_persons import get_persons_es_data

es = Elasticsearch(hosts='127.0.0.1:9200')

data = get_persons_es_data()
_index = 'persons'

bulk_query = []
for row in data:
    bulk_query.extend([
        json.dumps({'index':{'_index':_index, 
        '_id':str(row['id'])}}),
        json.dumps(row)
    ])
str_query = '\n'.join(bulk_query) + '\n'
response = es.bulk(str_query)

if response['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch')

