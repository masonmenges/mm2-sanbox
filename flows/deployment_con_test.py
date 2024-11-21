from prefect import flow, task
from prefect.runner.storage import GitRepository
import time

@task
def some_compute_task():
    time.sleep(1800) # Simulate a long running task
    return True

@flow
def main_flow():
    some_compute_task.map(return_state=True)

if __name__ == "__main__":
    main_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/deployment_con_test.py:main_flow",
    ).deploy(
        name="Deployment_con_test",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:demo_3",
        build=False,
        push=False,
        concurrency_limit=1
    )