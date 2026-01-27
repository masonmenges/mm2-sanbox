import os

from prefect import flow, task, get_run_logger
from prefect_aws import S3Bucket

from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule
import time

from prefect.cache_policies import DEFAULT, NONE, INPUTS


s3_bucket = S3Bucket.load("mm2-prefect-s3", _sync=True)
s3_bucket.bucket_folder = "cache_key"
cache_config = INPUTS.configure(
    key_storage=s3_bucket,
)

refresh_cache = os.getenv("REFRESH_CACHE", "False")


@task(cache_policy=cache_config, refresh_cache=refresh_cache)
def some_compute_task(a_number: int):
    logger = get_run_logger()

    logger.info(f"Computing {a_number} + 1")
    time.sleep(1800)
    return a_number + 1

@task(cache_policy=cache_config, refresh_cache=refresh_cache)
def sub_flow(a_number: int):
    some_compute_task(a_number)

@flow(persist_result=True)
def main_flow(a_number: int = 1):
    sub_flow(a_number)

if __name__ == "__main__":
    main_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/task_caching.py:main_flow",
    ).deploy(
        name="task_caching_ex",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:demo_3"
    )