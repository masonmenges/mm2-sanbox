import asyncio

from prefect import flow, task
from prefect_dbt.cloud.jobs import (
    trigger_dbt_cloud_job_run_and_wait_for_completion,
    TriggerJobRunOptions,
    get_dbt_cloud_run_artifact,
    )
from prefect_dbt.cloud.credentials import DbtCloudCredentials

dbt_cloud_credentials = DbtCloudCredentials.load("not-a-real-account")

async def run_dbt_model(job_id: int, model_name: str, is_snapshot=False):
    """
    Function to run dbt model
    :param is_snapshot: True if  the model is a snapshot
    :type is_snapshot: bool
    :param job_id: ID of the dbt job
    :type job_id: int
    :param model_name: Name of the dbt model
    :type model_name: str
    :return: Result of the dbt job run
    :rtype: dict
    :raises DbtCloudJobRunFailed: If the dbt job run fails
    :raises DbtCloudJobRunCancelled: If the dbt job run is cancelled
    """
    run_res = await trigger_dbt_cloud_job_run_and_wait_for_completion(
        dbt_cloud_credentials=dbt_cloud_credentials,
        job_id=job_id,
        trigger_job_run_options=TriggerJobRunOptions(
            steps_override=[f"""dbt {"snapshot" if is_snapshot else "run"} --select {model_name} """],
        ),
        retry_filtered_models_attempts=0,
        poll_frequency_seconds=10,
        max_wait_seconds=10800,
    )

    artifact = await get_dbt_cloud_run_artifact(
        dbt_cloud_credentials=dbt_cloud_credentials,
        run_id=run_res.get("id"),
        path="run_results.json"
    )
    results = artifact.get("results")
    warnings_tests = [f"{result.get('unique_id')} has returned with warnings in dbt" for result in results if
                      result.get("status") == "warn"]
    result = {"warnings": warnings_tests,
              "run_id": run_res.get("id"),
              "total_execution_time": artifact.get("elapsed_time"),
              }

    return result


@task(persist_result=True)
async def failing_dbt_task():
    """
    Flow to run a failing dbt model
    """
    run_res = await run_dbt_model(job_id=None, model_name="failing_model")

    if run_res.get("warnings"):
        raise ValueError(f"Dbt model failed with warnings: {run_res.get('warnings')}")

    return run_res

@flow  
async def failing_dbt_flow():
    """
    Flow to run a failing dbt model
    """
    await failing_dbt_task()


if __name__ == "__main__":
    # asyncio.run(failing_dbt_flow())

    from prefect.runner.storage import GitRepository, GitCredentials
    from prefect.client.schemas.schedules import CronSchedule
    from prefect.deployments import DeploymentImage
    failing_dbt_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
        entrypoint="flows/failing_dbt_flow_test.py:failing_dbt_flow",
    ).deploy(
    name="failing_dbt_demo_k8s",
    work_pool_name="k8s-minikube-test",
    version="failing_dbt_demo:0.0.7",
    enforce_parameter_schema=True,
    image=DeploymentImage(
    name="masonm2/temprepo:failing_dbt_flow",
    dockerfile="Dockerfile",
),
    )