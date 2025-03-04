from prefect import flow, task
from prefect.blocks.system import Secret
from prefect.runner.storage import GitRepository

@task
def fail(*args):
    raise ValueError("Failed")
 
@task
def succeed(*args):
    secret_block = Secret.load("toberemoved")

    return secret_block.get()
 
@flow
def final_state():
    _one = succeed()
    print(_one)
    _two = succeed(_one)
    print(_two)
    _three = succeed(_two)
    print(_three)
    return _three
 
if __name__ == "__main__":
    final_state.from_source(GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
    entrypoint="flows/test.py:final_state",
    ).deploy(
    name="secret state test", 
    work_pool_name="k8s-minikube-test",
    job_variables={"env": {"PREFECT_RESULTS_PERSIST_BY_DEFAULT": True, "PREFECT_LOCAL_STORAGE_PATH": "~/results/local"}, "image": "prefecthq/prefect:3.2.1-python3.12"}
    )