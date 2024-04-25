from prefect import flow, task
from state_change_hooks import cancel_if_already_running, cancel_if_already_running_async
import time


@task
def compute_task():
    time.sleep(180)
    print("computing...")


@flow(on_running=[cancel_if_already_running_async])
def running_flow():
    time.sleep(20)
    compute_task()
    

if __name__ == "__main__":
    running_flow()