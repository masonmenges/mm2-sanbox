from prefect import flow, task
from prefect.cache_policies import DEFAULT
from prefect_aws import S3Bucket

from prefect.runner.storage import GitRepository

cache_config = DEFAULT.configure(
    key_storage=S3Bucket.load("mm2-prefect-s3"),
)

@task(cache_policy=cache_config)
def some_compute_task(a_number: int):
    return a_number + 1

@flow(persist_result=True, result_storage=S3Bucket.load("mm2-prefect-s3"))
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