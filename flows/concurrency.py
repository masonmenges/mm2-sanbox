from prefect import flow, task, get_run_logger
from prefect.concurrency.sync import concurrency
import time

from prefect.deployments.runner import DeploymentImage 
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule


CONCURRENCY_CONFIG = "concurrency-test-limit-1"


@task
def long_running_task():
    logger = get_run_logger()

    logger.info(f"Using concurrency limit {CONCURRENCY_CONFIG}..")
    logger.info(f"Attempting to acquire concurrency limit slot..")

    with concurrency(CONCURRENCY_CONFIG, occupy=1):

        logger.info(f"Concurrency limit slot acquired..")

        time.sleep(600)

        logger.info(f"Concurrency slot released..")

    return None


@flow(name="Concurrency_Test_flow")
def con_flow():
    logger = get_run_logger()

    logger.info("Concurrency Task")
    df = long_running_task()


    return

if __name__ == "__main__":
    con_flow.from_source(
        source=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git"),
        entrypoint="flows/concurrency.py:con_flow",
    ).deploy(
        name="concurrency-test",
        work_pool_name="docker-test",
        image=DeploymentImage(
                    name="masonm2/temprepo:hello_flow",
                    dockerfile="./Dockerfile",
                ),
        schedule=CronSchedule(cron="0/5 * * * *", timezone="America/Denver")

    )