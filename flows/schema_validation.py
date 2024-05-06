# from pandera.typing import DataFrame, Series
from pydantic.types import List
from pydantic import BaseModel
from pandera import DataFrameModel
from pandera.engines.pandas_engine import PydanticModel
from prefect import flow, task, get_run_logger

# class SampleContract(BaseModel):
#     field_1: str
#     field_2: int

# class PydanticSampleContract(DataFrameModel):

#     class config:
#         dtype = PydanticModel(SampleContract)
#         coerce = True

class SampleContract(BaseModel):
    field_1: List[str]
    field_2: List[int]

# class PydanticSampleContract(BaseModel):
#     df: DataFrame[SampleContract]

class SampleContract2(BaseModel):
    fruit: List[str]

# class PydanticSampleContract2(BaseModel):
#     df: DataFrame[SampleContract2]

# class SampleContract2(BaseModel):
#     fruit: str

# class PydanticSampleContract2(DataFrameModel):
    
#     class config:
#         dtype = PydanticModel(SampleContract2)
#         coerce = True

@task
def add_fruits(input: SampleContract) -> SampleContract2:
    output = input.model_dump()
    output["fruit"] = ["apple", "banana"]
    return output


@flow(
    name="test_flow",
)
def test_flow(
    input: SampleContract = {"field_1": ["val1", "val2"], "field_2": [1, 2]},  # type: ignore[assignment]
) -> SampleContract2:
    logger = get_run_logger()
    logger.info(f"Data at Start of Flow: {input}")

    output = add_fruits(input)

    logger.info(f"Data at End of Flow: {output}")

    return SampleContract2.model_validate(output)  # type: ignore[return-value]


if __name__ == "__main__":
    test_flow()
