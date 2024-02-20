from prefect import flow, task, deploy
from prefect.deployments.runner import DeploymentImage 
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule
import time 
import random


@task
def compute_task():
    time.sleep(10)

@task
def secondary_task():
    print("I'm a second task!")
    time.sleep(5)

@flow
def demo_flow():
    compute_task()

    number = random.randint(1, 10)

    if number >= 5:
        secondary_task()

    return True


demo_flow()


if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git"),
        entrypoint="flows/demo.py:demo_flow",
    ).deploy(
        name="k8s-demo-test",
        work_pool_name="k8s-minikube-test",
        image=DeploymentImage(
                    name="masonm2/temprepo:demo_flow",
                    dockerfile="./Dockerfile",
                )
    )

