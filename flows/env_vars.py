from prefect import flow
from prefect.runner.storage import GitRepository  
import os

@flow(log_prints=True)
def env_vars_flow():
    print(os.environ.get("env_var_job_var_1"))
    print(os.environ.get("env_var_job_var_2"))
    print(os.environ.get("work_pool_env_1"))

if __name__ == "__main__":
    env_vars_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
        ),
        entrypoint="flows/env_vars.py:env_vars_flow"
    ).deploy(
        name="prefect_env_vars_test",
        work_pool_name="local_cloud_test",
        job_variables={
            "env_var_job_var_1": "value_1",
            "env_var_job_var_2": "value_2"
        }
    )