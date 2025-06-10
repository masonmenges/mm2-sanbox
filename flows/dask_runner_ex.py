from prefect import flow, task
from random import randint
import time
import asyncio

@task
async def my_task(time_seconds: int):
     time.sleep(time_seconds)
     return time_seconds

@flow(log_prints=True
     )
async def my_flow():
     ran_nums = [30, 60, 90, 120]
     futures = []

     futures = my_task.map(ran_nums)

     results = futures.result()
     print(results)


if __name__ == "__main__":
    asyncio.run(my_flow())