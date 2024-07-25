from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository
from prefect.deployments import DeploymentImage
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
async def demo_flow(date: str = None):
    logger = get_run_logger()
    logger.info(f"Hello World! {date}")
    # last_run_start_time = await compute_task()



if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
        entrypoint="flows/demo.py:demo_flow",
    ).deploy(
    name="params-test",
    work_pool_name="k8s-minikube-test",
    version="local_demo:0.0.5",
    enforce_parameter_schema=False,
    parameters=dict(date="2024-05-21"),
    image="masonm2/temprepo:demo_flow",
    build=False,
    job_variables=dict(
        service_account_name="prefect-test",
        env=dict(ENV_VAR_1="value1", ENV_VAR_2="value2")
        )
    )

