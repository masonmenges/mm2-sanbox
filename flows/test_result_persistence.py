from datetime import timedelta

from prefect import flow, task, get_client
from prefect.runner.storage import GitRepository
from prefect_aws import S3Bucket
from prefect.runtime import flow_run
from prefect.tasks import task_input_hash
from prefect.utilities.hashing import hash_objects


def cache_key_from_parent(context, parameters):
    subflow_id = context.task_run.flow_run_id
    # parent_id = flow_run.get_parent_flow_run_id()
    if parameters["parent_run_id"]:
        print("Parent run id is not None")
        return f"{parameters}"
    
    return hash_objects(
        context.task.task_key,
        parameters
        )


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
    print(flow_run.get_parent_flow_run_id())
    passing_task(parent_run_id=flow_run.get_parent_flow_run_id())
    subflow_caching()

@task(persist_result=True,
      cache_key_fn=cache_key_from_parent,
      cache_expiration=timedelta(days=1)
      )
def passing_task(some_param: int = 42, parent_run_id=None):
    print("This task should be skipped on retry")
    return 42

@task(persist_result=True)
def failing_task():
    raise ValueError("This task failed")

if __name__=="__main__":
    persist_test()
    # persist_test.from_source(
    #         source=GitRepository(
    #             url="https://github.com/masonmenges/mm2-sanbox.git"
    #             ),
    #         entrypoint="flows/test_result_persistence.py:persist_test",
    #     ).deploy(
    #     name="result_persistence-test_3.x",
    #     work_pool_name="default",
    #     )