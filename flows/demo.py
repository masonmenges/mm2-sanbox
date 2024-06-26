from prefect import flow, task, get_run_logger
import asyncio
from prefect import get_client
from prefect.client.schemas.filters import DeploymentFilterId, FlowRunFilterStateName, FlowRunFilter, DeploymentFilter
from prefect.client.schemas.sorting import FlowRunSort


@flow(retries=2, log_prints=True)
async def demo_flow():
    logger = get_run_logger()
    logger.info("This is a Windows Flow")
    # last_run_start_time = await compute_task()



if __name__ == "__main__":
    state = asyncio.run(demo_flow())

