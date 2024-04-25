from prefect import flow, task, get_run_logger
from prefect.concurrency.asyncio import concurrency
from prefect.deployments.runner import DeploymentImage 
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule
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

@task(timeout_seconds=45, retries=2)
async def secondary_task():
    await asyncio.sleep(5)


@flow(retries=2)
async def demo_flow(date: datetime):
    logger = get_run_logger()
    logger.info(date.tzinfo)

    async with concurrency(names=["concurrency-test-limit-1"]):
        await compute_task()

        number = random.randint(1, 10)

        if number >= 5:
            await secondary_task()

        return True


if __name__ == "__main__":
    # state = asyncio.run(demo_flow())

    # deploy from flow
    demo_flow.from_source(
            # source=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git"),
            source="~/Repos/git_hub_repos/sandbox/mm2-sanbox/flows/",
            entrypoint="demo.py:demo_flow",
        ).deploy(
            name="local-demo-test",
            work_pool_name="local-cloud-test",
            parameters={"date": "2024-03-21T00:00:00-06:00"},
            job_variables={
                "labels": {
                    "from_source": "deployment",
                    "env": "prod"
                    },
                "command": "conda run -n prefect_cloud_311 prefect flow-run execute"
            }
        )
