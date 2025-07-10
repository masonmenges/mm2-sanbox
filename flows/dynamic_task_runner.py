import os

from prefect import flow, task
from prefect_dask import DaskTaskRunner
from prefect.variables import Variable
from flow_utils.deployment_steps import get_num_workers_value

num_workers = get_num_workers_value()

    
@task
def some_task():
    pass

@flow(task_runner= DaskTaskRunner(cluster_kwargs={"n_workers": num_workers}))
def dynamic_task_runner_flow():

    some_task.submit().wait()

if __name__ == "__main__":
    dynamic_task_runner_flow()