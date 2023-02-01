import os
import asyncio
from socket import gaierror

import aioredis
import backoff


@backoff.on_exception(backoff.expo, gaierror)
async def wait_redis():
    redis = await aioredis.create_connection(os.environ.get("REDIS_URL"))
    redis.close()


if __name__ == "__main__":
    asyncio.run(wait_redis())
