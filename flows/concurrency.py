from prefect import flow, task, get_run_logger
from prefect.concurrency.asyncio import concurrency
from prefect.context import get_run_context
import datetime
import asyncio
import numpy as np

@task
async def group_a_task(n: int, run_name: str):

    count = 0
    a = 0
    b = 1

    sequence = []
    while count < n:
        sequence.append(a)
        ab = a + b
        a = b
        b = ab
        count +=1

    print(f"{run_name}:group a fibinacci sequence for {n} is {sequence}")


    return n + 1

@task
async def group_b_task(n: int, run_name: str):
    # logger = get_run_logger()
    # logger.info(f"sleep for {n}..")
    count = 0
    a = 0
    b = 1

    sequence = []
    while count < n:
        sequence.append(a)
        ab = a + b
        a = b
        b = ab
        count +=1

    print(f"{run_name}:group b fibinacci sequence for {n} is {sequence}")

@flow()
async def concurrent_flow(tasks):

    flow_run_name = get_run_context().flow_run.name

    group_a = [group_a_task(n, flow_run_name) for n in tasks]
    group_a_results = await asyncio.gather(*group_a)

    group_b = [group_b_task(n, flow_run_name) for n in group_a_results]
    await asyncio.gather(*group_b)



@flow(name="Concurrency_Test_flow_2")
async def con_flow(max_n: int = 10):
    tasks_groups = np.array_split(range(max_n), 2)
    subflows = [concurrent_flow(tasks) for tasks in tasks_groups]
    test = await asyncio.gather(*subflows, return_exceptions=True)



if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(con_flow())
    end = datetime.datetime.now()
    print(f"runtime: {end - start}")
