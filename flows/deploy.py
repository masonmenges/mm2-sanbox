from prefect.deployments.runner import DeploymentImage 
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule

from demo import demo_flow


demo_flow.from_source(
        source=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git"),
        entrypoint="flows/demo.py:demo_flow",
    ).deploy(
        name="ecs-demo-test",
        work_pool_name="ecs-test-pool",
        image=DeploymentImage(
                    name="masonm2/temprepo:demo_flow",
                    dockerfile="./Dockerfile",
                ),
        job_variables={
            "network_configuration": {
            "SecurityGroups": [
              "SG2"
            ],
            "Subnets": [
              "SUBNET2"
            ]
          }
        }
    )