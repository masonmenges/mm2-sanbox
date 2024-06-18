from prefect import flow, task
from prefect.runner.storage import GitRepository
from prefect.tasks import task_input_hash
from prefect.filesystems import LocalFileSystem

@flow(log_prints=True, result_storage=LocalFileSystem(basepath="/Users/masonmenges/Desktop/flowresults/"), persist_result=True)
def persist_test():
    passing_task()
    failing_task()

@task
def passing_task():
    print("This task should be skipped on retry")
    return 42

@task
def failing_task():
    raise ValueError("This task failed")

if __name__=="__main__":
    # persist_test.serve()

    persist_test.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/test_result_persistence.py:persist_test",
        ).deploy(
        name="result_persistence-test",
        work_pool_name="default",
        version="local_demo:0.0.1",
        # schedules=[schedule_1],
        enforce_parameter_schema=True,
        )