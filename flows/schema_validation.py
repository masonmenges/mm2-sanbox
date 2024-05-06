from pandera.typing import DataFrame, Series
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

class SampleContract(DataFrameModel):
    field_1: Series[str]
    field_2: Series[int]

class PydanticSampleContract(BaseModel):
    df: DataFrame[SampleContract]

class SampleContract2(DataFrameModel):
    fruit: Series[str]

class PydanticSampleContract2(BaseModel):
    df: DataFrame[SampleContract2]

# class SampleContract2(BaseModel):
#     fruit: str

# class PydanticSampleContract2(DataFrameModel):
    
#     class config:
#         dtype = PydanticModel(SampleContract2)
#         coerce = True

@task
def add_fruits(input: PydanticSampleContract) -> PydanticSampleContract2:
    output = input.df.copy()
    output["fruit"] = ["apple", "banana"]
    return {"df": output}


@flow(
    name="test_flow",
)
def test_flow(
    input: PydanticSampleContract = {"df": {"field_1": ["val1", "val2"], "field_2": [1, 2]}},  # type: ignore[assignment]
) -> PydanticSampleContract2:
    logger = get_run_logger()
    logger.info(f"Data at Start of Flow: {input}")

    output = add_fruits(input)

    logger.info(f"Data at End of Flow: {output}")

    return PydanticSampleContract2.model_validate(output)  # type: ignore[return-value]


if __name__ == "__main__":
    test_flow()
