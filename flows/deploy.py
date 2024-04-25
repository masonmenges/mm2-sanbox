from prefect.runner.storage import GitRepository, GitCredentials
from prefect.client.schemas.schedules import CronSchedule

from demo import demo_flow

schedule_1 = CronSchedule(cron="0 0 * * *")

demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
        entrypoint="flows/demo.py:demo_flow",
    ).deploy(
    name="local-demo-test",
    work_pool_name="k8s-minikube-test",
    version="local_demo:0.0.1",
    schedules=[schedule_1]
    )