from prefect import flow, get_run_logger
from prefect.runner.storage import GitRepository  
# from prefect_gcp.secret_manager import GcpSecret
import os

# from flows.task_caching import some_compute_task

@flow(log_prints=True, flow_run_name="TESTING ENV VARS")
def env_vars_flow():

    logger = get_run_logger()

    # gcpsecret_block = GcpSecret.load("mm2-test-secret", _sync=True, validate=False)
    # logger.info(gcpsecret_block.read_secret())

    print(os.environ.get("yaml_env_var_1"))
    print(os.environ.get("yaml_env_var_2"))
    print(os.environ.get("env_var_job_var_1"))
    print(os.environ.get("env_var_job_var_2"))
    print(os.environ.get("work_pool_env_1"))
    print(os.environ.get("test_secret"))

if __name__ == "__main__":
    env_vars_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
        ),
        entrypoint="flows/env_vars.py:env_vars_flow"
    ).deploy(
        name="prefect_env_vars_test",
        work_pool_name="k8s-minikube-test",
        job_variables={ "env": {{"name": "env_var_job_var_1", "value": "job_var1"}}}
    )
    # env_vars_flow()