from prefect import flow, task, get_run_logger

from prefect.settings import get_current_settings
from prefect.runner.storage import GitRepository
import json, os

@task
def child_task():
    logger = get_run_logger()
    logger.info("I'm a task log")


@flow
def child_flow():
    logger = get_run_logger()
    logger.info("I'm a subflow log")


@flow
def main():
    logger = get_run_logger()

    child_flow()
    child_task()

    test = get_current_settings().model_dump()

    logger.info(json.dumps(test, indent=2, default=str))

    logger.info("I'm done")




if __name__ == "__main__":
    main.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            commit_sha=os.getenv("GITHUB_SHA")
            ),
        entrypoint="flows/delay_testing.py:main"
        ).deploy(
        name="delay_testing",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:nocode05192025.1",
        build=False,
        push=False
    )