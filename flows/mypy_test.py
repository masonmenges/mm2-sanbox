from prefect import task


@task(name="Extract")
def extract() -> list[int]:
    return [1, 2, 3]