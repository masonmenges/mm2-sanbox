from prefect import flow, get_run_logger
from prefect.runner.storage import GitRepository  
from prefect_gcp.secret_manager import GcpSecret
import os

# from flows.task_caching import some_compute_task

@flow(log_prints=True)
def env_vars_flow():

    logger = get_run_logger()

    gcpsecret_block = GcpSecret.load("mm2-test-secret", _sync=True)
    logger.info(gcpsecret_block.read_secret())

    print(os.environ.get("yaml_env_var_1"))
    print(os.environ.get("yaml_env_var_2"))
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
        name="prefect_env_vars_test_vertex_ai",
        work_pool_name="mm2-vertextai-testing",
        job_variables={ "env": {
            "env_var_job_var_1": "job_value_1",
            "env_var_job_var_2": "job_value_2"
        }}
    )
