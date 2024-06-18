import asyncio
from prefect import task, flow
from random import randint

@task
async def math_fun(n: int):
    return n * n


@flow
async def my_flow(n):
    ran_nums = [randint(0, 100) for _ in range(n)]
    async with asyncio.TaskGroup() as tg:
        squared_nums = [tg.create_task(math_fun(num)) for num in ran_nums]


if __name__ == "__main__":
    asyncio.run(my_flow(n=50))