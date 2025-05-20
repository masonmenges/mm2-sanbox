import datetime, enum
from typing import List
from pydantic import BaseModel
from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
from prefect.artifacts import create_link_artifact
import asyncio, os, pytz

class SampleDropdownEnum(str, enum.Enum):
    positive="positvie"
    negatvie="negative"


class SampleValues(BaseModel):
    field_1: List[str]
    date: datetime.datetime = datetime.datetime.now().astimezone(pytz.timezone(("US/Denver")))
    dropdown: SampleDropdownEnum = SampleDropdownEnum.positive


@flow(log_prints=True)
async def demo_flow(params: SampleValues = SampleValues(field_1=["testing"])
):
    logger = get_run_logger()
    logger.info(f"Configs date: {params.date}")
    await create_link_artifact(link="notreal.notrel")


if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            commit_sha=os.getenv("GITHUB_SHA")
            ),
        entrypoint="flows/demo.py:demo_flow"
        ).deploy(
            name="param-testing",
            work_pool_name="local-worker-test"
        )
    open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
    print(open_api_schema)