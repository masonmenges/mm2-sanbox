from prefect import flow, task, get_run_logger, deploy, suspend_flow_run
import random
import sys
from functools import wraps
import time

def prefect_flow_on_completion(flow, flow_run, state):
    print("This is in an on_completion hook")
    return

def prefect_flow_on_failure(flow, flow_run, state):
    print("This is in an on_failure hook")
    return

def wrapped_flow(**kwargs):
    print("Do some action before flow runs")
    return flow(
        on_failure=[prefect_flow_on_failure],
        on_completion=[prefect_flow_on_completion],
        **kwargs
    )

@task
def some_long_running_task():
    logger = get_run_logger()
    logger.info("This is a long running task")
    time.sleep(180)

@wrapped_flow()
def hello_flow():
    logger = get_run_logger()
    logger.info("Hello world!")
    random_number = random.randint(1, 10)

    task_futures = [some_long_running_task.submit() for _ in range(5)]

    # if random_number % 2 == 0:
    #     raise ValueError("Random number is even, so we'll fail the flow")
    # else:
    return


if __name__ == "__main__":
    hello_flow()
    # test = hello_flow.to_deployment(
    # name=f"decorated_and_wrapped_flow"
    # )
    # test.storage=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git")
    # test.entrypoint = "flows/wrapped_flow_test.py:hello_flow"
    # deploy(
    #     test,
    #     work_pool_name="docker-test",
    #     image=DeploymentImage(
    #                 name="masonm2/temprepo:hello_flow",
    #                 dockerfile="./Dockerfile",
    #             ))