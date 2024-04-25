from prefect import flow, task
from state_change_hooks import cancel_if_already_running
import time


@task
def compute_task():
    time.sleep(180)
    print("computing...")


@flow(on_running=[cancel_if_already_running])
def running_flow():
    compute_task()
    

if __name__ == "__main__":
    running_flow()