from pandera.typing import DataFrame, Series
from pandera import DataFrameModel
from prefect import flow, task, get_run_logger
import pandas as pd


class SampleContract(DataFrameModel):
    field_1: Series[str]
    field_2: Series[int]


class SampleContract2(DataFrameModel):
    fruit: Series[str]


@task
def add_fruits(input: DataFrame[SampleContract]) -> DataFrame[SampleContract2]:
    output = input.copy()
    output["fruit"] = ["apple", "banana"]
    return output


@flow(
    name="test_flow",
)
def test_flow(
    input: DataFrame[SampleContract] = pd.DataFrame({"field_1": ["val1", "val2"], "field_2": [1, 2]})
) -> DataFrame[SampleContract2]:
    logger = get_run_logger()
    logger.info(f"Data at Start of Flow: {input}")

    output = add_fruits(input)

    logger.info(f"Data at End of Flow: {output}")

    return SampleContract2.validate(output)


if __name__ == "__main__":
    test_flow()