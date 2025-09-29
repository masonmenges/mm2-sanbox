import asyncio, os

from prefect import flow, task, get_run_logger
from prefect.futures import wait

from prefect.runner.storage import GitRepository


@task
async def long_running_task():
    logger = get_run_logger()
    try:
        while True:
            await asyncio.sleep(5)

    except asyncio.CancelledError:
        logger.warning(f"got cancellation signal!")
        raise

    except Exception as ex:
        logger.error(f" got unexpected exception: {ex}")
        raise


@flow(log_prints=True)
async def long_running_flow():
    logger = get_run_logger()
    tasks = []
    results = []

    for _ in range(0, 10):
        task = long_running_task.submit()
        tasks.append(task)
    logger.info(f"All tasks submitted!")

    wait(tasks)    

    try:
        for task in tasks:
            results.append(task.result())
    except asyncio.CancelledError:
        logger.warning(f"main flow got manual cancellation! Notifying all tasks...")
        for task in tasks:

            task.cancel()
        raise
    except Exception as ex:
        logger.error(f"main flow unexpected failed: {ex}")
        raise

if __name__ == "__main__":
    long_running_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            commit_sha=os.getenv("GITHUB_SHA")
            ),
        entrypoint="flows/long_running_test.py:long_running_flow"
        ).deploy(
            name="long-running-testing",
            work_pool_name="demo_eks",
            image="455346737763.dkr.ecr.us-east-2.amazonaws.com/mm2/flowsa:lowerwebsocketsversion",
            build=False,
            push=False
        )
    

