from prefect import flow

from prefect.runner.storage import GitRepository

from random import randint


def rand_failure(retry_count=3):
    randnum = randint(0, 1)
    for i in range(retry_count):
        try:
            print(f"Attempt {i + 1} of {retry_count}")
            if randnum == 0:
                raise ValueError("This is an error")
            break
        except Exception as e:
            print(f"Error: {e}")
            randnum = randint(0, 1)
            continue
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

