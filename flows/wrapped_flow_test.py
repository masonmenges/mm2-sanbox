from prefect import flow, task, get_run_logger
import smtplib
import os
import random
import functools
import sys
from prefect.runner.storage import GitRepository
from prefect.blocks.system import Secret
from functools import wraps



    
def prefect_flow_on_completion(flow, flow_run, state):
    print("This is in an on_completion hook")
    return

def prefect_flow_on_failure(flow, flow_run, state):
    print("This is in an on_failure hook")
    return


def wrapped_flow(**kwargs):
    return flow(
        on_failure=[prefect_flow_on_failure],
        on_completion=[prefect_flow_on_completion],
        **kwargs
    )

def email_with_args(msg, email):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            print("Extra logic here")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator


@email_with_args(
    msg="This is in the start wrapper",
    email="mason@prefect.io")
@wrapped_flow()
def hello_flow():
    logger = get_run_logger()
    logger.info("Hello world!")
    logger.info("Going to send an email now...")
    random_number = random.randint(1, 10)

    if random_number % 2 == 0:
        raise ValueError("Random number is even, so we'll fail the flow")
    else:
        return 


if __name__ == "__main__":
    # hello_flow()
    flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
        ),
        entrypoint="flows/wrapped_flow_test.py:hello_flow"
    ).deploy(
        name=f"decorated_and_wrapped_flow",
        work_pool_name="local-dev",
        build=False
    )