import os

from prefect import flow, task
from prefect_dask import DaskTaskRunner
from prefect.variables import Variable
from prefect import context

    
@task
def some_task():
    pass

@flow(task_runner= DaskTaskRunner(cluster_kwargs={"n_workers": int(os.environ.get("num_workers", "Not Set"))}))
def dynamic_task_runner_flow():

    some_task.submit().wait()

if __name__ == "__main__":
    dynamic_task_runner_flow()