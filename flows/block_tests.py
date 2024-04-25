from prefect import flow, task

from prefect.deployments.deployments import Deployment
from prefect.client.schemas.schedules import CronSchedule

from prefect.tasks import task_input_hash

@task(cache_key_fn=task_input_hash)
def cached_task():
    return "I'm a cached task!"

@flow
def caching_flow(rerun: str= False):
    cached_task.with_options(refresh_cache=rerun)()


if __name__ == "__main__":

    schedule1 = CronSchedule(cron="0 1 * * *")

    Deployment.build_from_flow(
        name="caching_flow", 
        flow=caching_flow,
        schedules=[
            {"schedule": schedule1, 
             "active": False
             }
             ],
        apply=True
        )
    