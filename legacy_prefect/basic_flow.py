from prefect import flow

from prefect.runner.storage import GitRepository

from random import randint


@flow(retries=3, retry_delay_seconds=600, log_prints=True)
def basic_flow():
    
    raise ValueError("This is a test error")

if __name__ == "__main__":
    basic_flow()

    # basic_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git"
    #         ),
    #     entrypoint="legacy_prefect/basic_flow.py:basic_flow",
    # ).deploy(
    # name="basic_flow_retries",
    # work_pool_name="k8s-minikube-test",
    # image=DockerImage(
    # name="masonm2/temprepo:basic_flow",
    # dockerfile="Dockerfile",
    # )
    # )

