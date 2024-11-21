from prefect import flow, task
from prefect.concurrency.sync import rate_limit, concurrency
from prefect.deployments import run_deployment
import time, asyncio

@task
async def trigger_deployment():
    rate_limit(names="submission_limit", occupy=1)

    with concurrency("local_test", occupy=1):
        asyncio.sleep(3)


@flow
async def main_flow():
    for _ in range(100):
        trigger_deployment.submit()


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main_flow())
    end = time.time()
    print(f"Total time: {end - start}")