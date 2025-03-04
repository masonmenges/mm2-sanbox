from prefect import flow, task
from prefect.blocks.system import Secret

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
    test = final_state()