import os

from prefect import flow, task
from prefect_dask import DaskTaskRunner
from prefect.variables import Variable
from prefect import context

    
@task
def some_task():
    pass

@flow(task_runner= DaskTaskRunner(cluster_kwargs={"n_workers": int(os.environ["num_workers"])}))
def dynaimc_task_runner_flow():

    some_task.submit().wait()

if __name__ == "__main__":
    dynaimc_task_runner_flow()