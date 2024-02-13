from prefect import flow, task, deploy
import time 
import random


@task
def compute_task():
    time.sleep(10)

@task
def secondary_task():
    print("I'm a second task!")
    time.sleep(5)

@flow
def demo_flow():
    compute_task()

    number = random.randint(1, 10)

    if number >= 5:
        secondary_task()

    return True


