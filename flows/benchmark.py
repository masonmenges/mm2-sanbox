import asyncio
import time
from prefect import flow, task

@task
def sync_add_one(n):
    return n + 1


@flow
def sync_add_flow():
    res = 0
    for i in range(100):
        res = sync_add_one(res)
    return res

@task
async def add_one(n):
    return n + 1


@flow
async def add_flow():
    res = 0
    for i in range(100):
        res = await add_one(res)
    return res


if __name__ == '__main__':
    s = time.time()
    sync_add_flow()
    e = time.time()
    sync_time = e - s

    s2 = time.time()
    asyncio.run(add_flow())
    e2 = time.time()
    async_time = e2 - s2

    print(f"Sync time: {sync_time:.2f} s")
    print(f"Async time: {async_time:.2f} s")