from prefect import flow
from prefect_dbt.cloud import DbtCloudJob
from prefect_dbt.cloud.jobs import run_dbt_cloud_job
import asyncio

@flow
async def run_dbt_job_flow():
    result = await run_dbt_cloud_job(
        dbt_cloud_job=await DbtCloudJob.load("dbt-cloud-job"),
        targeted_retries=0,
    )
    return await result

if __name__ == "__main__":
    asyncio.run(run_dbt_job_flow())