import requests
import aiohttp

url = 'http://10.4.3.111:8082/api/v1/persons/search'

req = requests.get('http://10.4.3.111:8082/api/v1/persons/search?search_by_title=Ann&page%5Bnumber%5D=1&page%5Bsize%5D=50')
print(len(req.json()))


async def t1():
    session = aiohttp.ClientSession()
    d = {}


    async with session.get(url, params={'search_by_title': 'Ann'}) as response:
        d['body'] = response.json()
        d['headers'] = response.headers
        d['status'] = response.status

    session.close()

    return d

await t1
print(r)