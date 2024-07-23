from prefect import flow, task, get_run_logger
from prefect.concurrency.asyncio import concurrency
import datetime
import asyncio
import numpy as np


@task
async def group_a_task(n: int):
    # logger = get_run_logger()
    # logger.info(f"sleep for {n}..")
    print(f"sleep for {n}..")
    await asyncio.sleep(n)
    return n+1

@task
async def group_b_task(n: int):
    # logger = get_run_logger()
    # logger.info(f"sleep for {n}..")
    print(f"sleep for {n}..")
    await asyncio.sleep(n)

@flow
async def concurrent_flow(tasks):
    # logger = get_run_logger()
    # logger.info("Proccessing tasks: %s", tasks)
    # async with concurrency("local_test", occupy=len(tasks)):

    group_a = [group_a_task(5) for n in tasks]
    group_a_results = await asyncio.gather(*group_a)

    group_b = [group_b_task(n) for n in group_a_results]
    await asyncio.gather(*group_b)


@flow(name="Concurrency_Test_flow_2")
async def con_flow():
    tasks_groups = np.array_split(range(40), 5)
    print("Concurrency Task")
    subflows = [concurrent_flow(tasks) for tasks in tasks_groups]
    await asyncio.gather(*subflows)

if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(con_flow())
    end = datetime.datetime.now()
    print(f"runtime: {end - start}")
