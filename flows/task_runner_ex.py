from prefect import flow, task
from prefect.task_runners import ThreadPoolTaskRunner


@task
def some_task(input: str):
    print("Task: " + input)
    print("task doing task things")


@flow(task_runner=ThreadPoolTaskRunner) 
def some_flow():
    some_task("a")
    some_task.submit("b").wait()

some_flow()