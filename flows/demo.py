import datetime, enum
from typing import List
from pydantic import BaseModel
from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
from prefect.artifacts import create_link_artifact
import asyncio

class SampleDropdownEnum(str, enum.Enum):
    positive="positvie"
    negatvie="negative"


class SampleValues(BaseModel):
    field_1: List[str]
    date: datetime.datetime
    dropdown: SampleDropdownEnum = SampleDropdownEnum.positive


@flow(log_prints=True)
async def demo_flow(date: str = "2025-05-20"):
    logger = get_run_logger()
    logger.info(f"Configs date: {date}")
    await create_link_artifact(link="notreal.notrel")


open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
print(open_api_schema)

if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/demo.py:demo_flow"
        ).deploy(
            name="param-testing",
            work_pool_name="local-worker-test"
        )
    open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
    print(open_api_schema)
    asyncio.run(demo_flow("2024-11-14"))