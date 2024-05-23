from prefect import flow, task, get_run_logger
import asyncio
from prefect import get_client
from prefect.client.schemas.filters import DeploymentFilterId, FlowRunFilterStateName, FlowRunFilter, DeploymentFilter
from prefect.client.schemas.sorting import FlowRunSort

# from state_change_hooks import cancel_if_already_running


# @task
# async def compute_task():
#     async with get_client() as client:
        # dep = await client.read_deployment("799c5f9f-7e84-4257-8f79-493b494ba244")



        # flow_runs = await client.read_flow_runs(
        #     flow_run_filter=FlowRunFilter(state=FlowRunFilterStateName(any_ = ["Completed"])),
        #     deployment_filter=DeploymentFilter(id = DeploymentFilterId(any_ = ["799c5f9f-7e84-4257-8f79-493b494ba244"])),
        #     sort=FlowRunSort.START_TIME_DESC,
        #     )
        
        # return flow_runs[0].start_time      

@flow(retries=2, log_prints=True)
async def demo_flow(date: str):
    logger = get_run_logger()
    logger.info(date)
    # last_run_start_time = await compute_task()



if __name__ == "__main__":
    state = asyncio.run(demo_flow())

