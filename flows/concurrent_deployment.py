import asyncio

from prefect import task, flow
from prefect.client.schemas import FlowRun
from prefect.deployments import run_deployment
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.runner.storage import GitRepository
from prefect_aws.deployments.steps import push_to_s3, pull_from_s3


@flow(task_runner=ThreadPoolTaskRunner(max_workers=5), log_prints=True)
def parent_flow():
    # run the run_deployment_of_child_flow task via the ThreadPoolTaskRunner and wait for the
    #  result and return the result

    run = run_deployment(
        name="persist-test/result_persistence-test_3"
    )

    print(run.state.result(fetch=True))

if __name__ == "__main__":
    # parent_flow.from_source(
    #         source=GitRepository(
    #             url="https://github.com/masonmenges/mm2-sanbox.git"
    #             ),
    #         entrypoint="flows/concurrent_deployment.py:parent_flow",
    #     ).deploy(
    #     name="parent_run_deployment_test",
    #     work_pool_name="k8s-minikube-test",
    #     image="masonm2/temprepo:withcode03132025.3",
    #     build=False,
    #     push=False
    #     )
    parent_flow()