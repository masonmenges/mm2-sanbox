import datetime, enum
from typing import List
from pydantic import BaseModel
from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
from prefect.artifacts import create_link_artifact
import asyncio, os, pytz

from prefect.runtime.flow_run import get_job_variables

from prefect.task_runners import ThreadPoolTaskRunner

test = get_job_variables()

class SampleDropdownEnum(str, enum.Enum):
    positive="positvie"
    negatvie="negative"


class SampleValues(BaseModel):
    field_1: List[str]
    date: datetime.datetime = datetime.datetime.now().astimezone(pytz.timezone(("US/Mountain")))
    dropdown: SampleDropdownEnum = SampleDropdownEnum.positive


@task()
def some_task():
    pass



@flow(flow_run_name=test["Name"])
def demo_flow(date: str = None):
    logger = get_run_logger()
    logger.info(f"Configs date: {date}")
    

    some_task()


if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            commit_sha=os.getenv("GITHUB_SHA")
            ),
        entrypoint="flows/demo.py:demo_flow"
        ).deploy(
            name="custom-name-testing",
            work_pool_name="k8s-minikube-test",
            job_variables={
                "name": "custom-job-name"
            }
        )
    # open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
    # print(open_api_schema)
    # asyncio.run(demo_flow())