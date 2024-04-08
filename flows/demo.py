from prefect import flow, task, get_run_logger
from prefect.concurrency.asyncio import concurrency
import asyncio
import random
from prefect import get_client
from datetime import datetime

from state_change_hooks import cancel_if_already_running


@task
async def compute_task():
    async with get_client() as client:
        dep = await client.read_deployment("799c5f9f-7e84-4257-8f79-493b494ba244")
        print(dep.name)

@task
async def secondary_task():
    await asyncio.sleep(5)


@flow(retries=2, log_prints=True)
async def demo_flow(date: datetime):
    logger = get_run_logger()
    logger.info("Running demo flow with logger statement")

    print("Running demo flow with print statement")

    async with concurrency(names=["concurrency-test-limit-1"]):
        await compute_task()

        number = random.randint(1, 10)

        if number >= 5:
            await secondary_task()

        return True


if __name__ == "__main__":
    state = asyncio.run(demo_flow())

