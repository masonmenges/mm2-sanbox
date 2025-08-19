import datetime, enum
from typing import List
from pydantic import BaseModel, Field
from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
import os, pytz, datetime


class AssetsToActOnEnum(enum.StrEnum):
    ThingOne = 'thing_one'
    ThingTwo = 'MyGreatThingy'
    ThingThree = 'AlsoACoolThing'

class SampleDropdownEnum(enum.StrEnum):
    positive="positvie"
    negatvie="negative"

print(list(SampleDropdownEnum))


class SampleValues(BaseModel):
    date: datetime.datetime = Field(title="Date", default_factory = lambda: datetime.datetime.today().astimezone(pytz.timezone(("US/Mountain"))))
    dropdown: List[AssetsToActOnEnum |SampleDropdownEnum] = list(SampleDropdownEnum)


@task()
def some_task():
    pass

@flow()
def demo_flow(configs: SampleValues):

    logger = get_run_logger()
    logger.info(f"Configs date: {configs.date}")
    
    some_task()


if __name__ == "__main__":
    demo_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            commit_sha=os.getenv("GITHUB_SHA")
            ),
        entrypoint="flows/demo.py:demo_flow"
        ).deploy(
            name="dynamic-parameter-test",
            work_pool_name="demo_eks"
        )
    # open_api_schema = demo_flow.to_deployment(name="false")._parameter_openapi_schema.model_dump()
    # print(open_api_schema)
    # asyncio.run(demo_flow())