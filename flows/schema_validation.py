from pydantic import BaseModel 
from pydantic.types import List
from prefect import flow, task, get_run_logger

class SampleContract(BaseModel):
    field_1: List[str]
    field_2: List[int]


class SampleContract2(BaseModel):
    fruit: List[str]


# @task
def add_fruits(input: SampleContract) -> SampleContract2:
    output = input.model_dump()
    output["fruit"] = ["apple", "banana"]
    return output


# @flow(
#     name="test_flow",
#     validate_parameters=True
# )
def test_flow(
    input: SampleContract = SampleContract.model_validate({"field_1": ["val1", "val2"], "field_2": [1, 2]}),  # type: ignore[assignment]
) -> SampleContract2:
    # logger = get_run_logger()
    # logger.info(f"Data at Start of Flow: {input}")

    output = add_fruits(input)

    # logger.info(f"Data at End of Flow: {output}")

    return SampleContract2.model_validate(output)  # type: ignore[return-value]


if __name__ == "__main__":
    test_flow(input={"field_1": ["val1", "val2"], "field_2": [1, 2]})
