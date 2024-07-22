from prefect import flow, task, get_run_logger
import os
from prefect.concurrency.asyncio import concurrency, rate_limit
import datetime
import asyncio
import numpy as np


@task
async def long_running_task(n: int):
    logger = get_run_logger()
    logger.info(f"Task {n} running..")
    await asyncio.sleep(5)

@flow
async def concurrent_flow(tasks):
    logger = get_run_logger()
    logger.info("Proccessing tasks: %s", tasks)
    async with concurrency("local_test", occupy=len(tasks)):
        results = [long_running_task(n) for n in tasks]
        await asyncio.gather(*results)

@flow(name="Concurrency_Test_flow_2", timeout_seconds=os.environ.get("TIMEOUT_SECONDS", 60))
async def con_flow():
    tasks_groups = np.array_split(range(40), 5)
    print("Concurrency Task")
    for tasks in tasks_groups:
        await concurrent_flow(tasks)


if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(con_flow())
    end = datetime.datetime.now()
    print(f"runtime: {end - start}")
