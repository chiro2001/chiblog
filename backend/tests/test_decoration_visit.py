import requests
from tqdm import trange
import asyncio
import random


async def request_one(username: str, password: str):
    js = requests.get(f"http://127.0.0.1:8192/api/v1/user/1?username={username}&password={password}").json()
    print(js['data']['username'] == username and js['data']['password'] == password, js)


async def test_main():
    tasks = []
    for i in trange(100000):
        tasks.append(request_one('%s' % i, '%s' % i))
        # await request_one('%s' % random.randint(1 + i, 100 + i), '%s' % random.randint(1 + i, 100 + i))
        # await asyncio.sleep(0.2)
    for t in tasks:
        await t


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(test_main())
    asyncio.run(test_main())

