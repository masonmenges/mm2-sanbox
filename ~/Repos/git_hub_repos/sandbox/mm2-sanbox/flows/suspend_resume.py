import time
import os
from prefect import task, flow
from prefect_dask import DaskTaskRunner


from dask_kubernetes.operator import KubeCluster


# print(os.environ.get("KUBECONFIG", "~/.kube/config"))


# cluster = KubeCluster(name="prefect-dask-cluster",
#  image='ghcr.io/dask/dask:latest',
#  n_workers=2,
#  resources={"requests": {"memory": "0.5Gi"}, "limits": {"memory": "1.5Gi"}},
#  env={"FOO" : "barr"}
#  )



@task
def some_task():
    print("Hello world!")
    time.sleep(10)

@flow(task_runner=DaskTaskRunner(address="127.0.0.1:8080"))
def dask_test_flow():
    results = [some_task.submit() for _ in range(2)]


dask_test_flow()

