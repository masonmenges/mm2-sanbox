from prefect import flow

from prefect.runner.storage import GitRepository

from random import randint


def rand_failure(retry_count=3):
    for i in range(retry_count):
        try:
            print(f"Attempt {i} of {retry_count}")
            raise ValueError("This is an error")
        except Exception as e:
            print(f"Error: {e}")
            if i == retry_count - 1:
                raise e
    return True


@flow(retries=3, retry_delay_seconds=5, log_prints=True)
def basic_flow():
    
    rand_failure()
    
    return "This is a success"

if __name__ == "__main__":
    basic_flow()

    # basic_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git"
    #         ),
    #     entrypoint="legacy_prefect/basic_flow.py:basic_flow",
    # ).deploy(
    # name="basic_flow_retries",
    # work_pool_name="k8s-minikube-test",
    # image=DockerImage(
    # name="masonm2/temprepo:basic_flow",
    # dockerfile="Dockerfile",
    # )
    # )

