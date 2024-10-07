from prefect import flow, task, get_run_logger
from prefect.cache_policies import DEFAULT
from prefect_aws import S3Bucket

from prefect.runner.storage import GitRepository
import time

s3_bucket = S3Bucket.load("mm2-prefect-s3", _sync=True)
s3_bucket.bucket_folder = "cache_key"
cache_config = DEFAULT.configure(
    key_storage=s3_bucket,
)

@task
def some_compute_task(a_number: int):
    logger = get_run_logger()

    logger.info(f"Computing {a_number} + 1")
    time.sleep(1800)
    return a_number + 1

@flow(persist_result=True, result_storage=S3Bucket.load("mm2-prefect-s3", _sync=True))
def main_flow(a_number: int = 1):
    some_compute_task(a_number)

if __name__ == "__main__":
    main_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/task_caching.py:main_flow",
    ).deploy(
        name="task_caching",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:demo_3",
        build=False,
        push=False
    )