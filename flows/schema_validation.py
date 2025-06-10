from pydantic import BaseModel 
from pydantic.types import List
import enum
import datetime
from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository

class SampleDropdownEnum(str, enum.Enum):
    positive="positvie"
    negatvie="negative"


class SampleValues(BaseModel):
    field_1: List[str]
    date: datetime.datetime
    dropdown: SampleDropdownEnum = SampleDropdownEnum.positive

@flow(
    name="test_flow",
    validate_parameters=True
)
def test_flow(
    input: SampleValues = {"field_1": ["val1", "val2"], "date": datetime.date(2025, 3, 21)},  # type: ignore[assignment]
):
    logger = get_run_logger()
    logger.info(f"Data at Start of Flow: {input}")


if __name__ == "__main__":
    test_flow.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/schema_validation.py:test_flow",
        ).deploy(
        name="UI_param_test",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:withcode03132025.3",
        build=False,
        push=False
        )
