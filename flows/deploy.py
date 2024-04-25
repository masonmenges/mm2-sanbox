from prefect.runner.storage import GitRepository, GitCredentials
from prefect.client.schemas.schedules import CronSchedule

from demo import demo_flow
from final_state_from_task import running_flow

schedule_1 = {"schedule": CronSchedule(cron="0 0 * * *"), "active": False}

running_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
        entrypoint="flows/final_state_from_task.py:running_flow",
    ).deploy(
    name="on_running_cancel",
    work_pool_name="k8s-minikube-test",
    version="local_demo:0.0.1",
    schedules=[schedule_1]
    )