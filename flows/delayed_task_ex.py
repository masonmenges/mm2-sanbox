from prefect import flow, task
from background_tasks.delayed_task import background_task

@task
def quick_task():
    print("just a quick check")

@flow
def parent_app():
    a = background_task.delay()

    b = quick_task.submit(wait_for=[a]).wait()

parent_app()

    