import os 

from prefect.deployments.steps import git_clone

from random import randint

def get_num_workers_value(depname: str):
    num_workers = randint(1, 8)

    os.environ["num_workers"] = str(num_workers)

    print(os.environ["num_workers"])