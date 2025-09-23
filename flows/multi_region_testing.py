from prefect import flow, task, get_run_logger
from prefect.context import get_run_context
from prefect.runner.storage import GitRepository  
from prefect.concurrency.sync import concurrency
import os, time
from pprint import pprint

@task(retries=2, log_prints=True)
def some_task():
    time.sleep(20)
    context = get_run_context()
    print(context.task_run.run_count)
    if context.task_run.run_count > 1:
        return "success"
    raise ValueError("I'm a Failure")

@flow()
def demo_flow():
    logger = get_run_logger()

    concurrency_limit_name = os.getenv("CONCURRENCY_LIMIT_NAME", "local")

    with concurrency(concurrency_limit_name, occupy=1): 
        some_task()


if __name__ == "__main__":
    # demo_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git",
    #         commit_sha=os.getenv("GITHUB_SHA")
    #         ),
    #     entrypoint="flows/multi_region_testing.py:demo_flow"
    #     ).deploy(
    #         name="dynamic-parameter-test",
    #         work_pool_name="demo_eks",
    #         job_variables={
    #             "env": {
    #                 "PREFECT_FLOW_RUN_EXECUTE_SIGTERM_BEHAVIOR": "false"
    #             },
    #             "backoff_limit": 1
    #         }
    #     )
    # open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
    # pprint(open_api_schema)
    demo_flow()