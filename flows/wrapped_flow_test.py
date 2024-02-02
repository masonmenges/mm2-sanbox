from prefect import flow, task, get_run_logger, deploy
from prefect.runner.storage import GitRepository
from prefect.deployments.runner import DeploymentImage 
import random
import sys
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

@wrapped_flow()
def hello_flow():
    logger = get_run_logger()
    logger.info("Hello world!")
    random_number = random.randint(1, 10)

    if random_number % 2 == 0:
        raise ValueError("Random number is even, so we'll fail the flow")
    else:
        return


if __name__ == "__main__":
    # hello_flow()

    test = hello_flow.to_deployment(
    name=f"decorated_and_wrapped_flow"
    )
    test.storage=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git")
    test.entrypoint = "flows/wrapped_flow_test.py:hello_flow"
    print(test)

    deploy(
        test,
        work_pool_name="docker-test",
        image=DeploymentImage(
                    name="masonm2/temprepo:hello_flow",
                    dockerfile="./Dockerfile",
                ))