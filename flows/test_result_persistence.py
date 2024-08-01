from datetime import timedelta

from prefect import flow, task
from prefect.runner.storage import GitRepository
from prefect.tasks import task_input_hash
from prefect.runtime import flow_run
from prefect_aws import S3Bucket


def cache_key_from_parent(context, parameters):
    parent_id = context.flow_run_id
    print(parent_id)
    return parent_id

@flow
def subflow_caching():
    passing_task()

@flow(
        log_prints=True,
        result_storage=S3Bucket.load("mm2-prefect-s3"),
        persist_result=True,
        retries=1
        )
def persist_test():
    passing_task()
    subflow_caching()

@task(persist_result=True,
      cache_key_fn=cache_key_from_parent,
      cache_expiration=timedelta(days=1)
      )
def passing_task():
    print("This task should be skipped on retry")
    return 42

@task(persist_result=True)
def failing_task():
    raise ValueError("This task failed")

if __name__=="__main__":
    persist_test.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/test_result_persistence.py:persist_test",
        ).deploy(
        name="result_persistence-test_3.x",
        work_pool_name="default",
        )