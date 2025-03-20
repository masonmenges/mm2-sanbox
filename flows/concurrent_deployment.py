import asyncio

from prefect import task, flow
from prefect.client.schemas import FlowRun
from prefect.deployments import run_deployment
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.runner.storage import GitRepository


@task
def run_deployment_of_child_flow(deployment_name: str) -> FlowRun:
    flow_run = run_deployment(
        name=deployment_name
    )
    return flow_run  # noqa


@flow(task_runner=ThreadPoolTaskRunner(max_workers=5))
async def parent_flow():
    # run the run_deployment_of_child_flow task via the ThreadPoolTaskRunner and wait for the
    #  result and return the result
    flow_run_futures = run_deployment_of_child_flow.map(["persist-test/result_persistence-test_3"])

    flow_runs = flow_run_futures.result()

    for x in flow_runs:
        result_val = await x.state.result(fetch=True)
        print(result_val)


if __name__ == "__main__":
    parent_flow.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/concurrent_deployment.py:parent_flow",
        ).deploy(
        name="parent_run_deployment_test",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:withcode03132025.2",
        build=False,
        push=False
        )