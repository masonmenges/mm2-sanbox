from prefect.deployments.runner import DeploymentImage 
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule

from prefect import deploy

from demo import demo_flow
from local_dev_flow import check_flow_deployment_version




# demo_flow.from_source(
#         source=GitRepository(url="https://github.com/masonmenges/mm2-sanbox.git"),
#         entrypoint="flows/demo.py:demo_flow",
#     ).deploy(
#     name="local-demo-test",
#     work_pool_name="default-agent-pool",
#     ),
check_flow_deployment_version.from_source(
        source="./flows/",
        entrypoint="local_dev_flow.py:check_flow_deployment_version",
    ).deploy(
    name="local-dev-test",
    work_pool_name="worker-local-dev",
    version="local_dev:0.0.1",
)

