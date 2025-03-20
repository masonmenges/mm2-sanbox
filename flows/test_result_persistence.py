from datetime import timedelta

from prefect import flow, task, get_client
from prefect.runner.storage import GitRepository
from prefect_aws import S3Bucket
from prefect.runtime import flow_run
from prefect.tasks import task_input_hash
from prefect.utilities.hashing import hash_objects


@flow
def subflow_caching():
    print(flow_run.get_parent_flow_run_id())
    passing_task(parent_run_id=flow_run.get_parent_flow_run_id())

@flow(
        log_prints=True,
        result_storage=S3Bucket.load("mm2-prefect-s3"),
        persist_result=True,
        retries=1
        )
def persist_test():
    passing_task(parent_run_id=flow_run.get_parent_flow_run_id())
    subflow_caching()

    return 42

@task(persist_result=True
      )
def passing_task(some_param: int = 42, parent_run_id=None):
    print("This task should be skipped on retry")
    return 42

@task(persist_result=True)
def failing_task():
    raise ValueError("This task failed")

if __name__=="__main__":
    # persist_test()
    persist_test.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/test_result_persistence.py:persist_test",
        ).deploy(
        name="result_persistence-test_3.x",
        work_pool_name="k8s-minikube-test",
        )