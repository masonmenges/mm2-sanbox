from prefect import flow, task

import asyncio

@task
async def some_compute_task(a_number: int):
    await asyncio.sleep(3)

    print(f"Computing {a_number} + 1")
    new_number = a_number + 1
    if new_number % 2 == 0:
        return new_number
    raise ValueError(f"Number {new_number} is not even")

@flow
async def sub_flow(a_number: int):
    await some_compute_task(a_number)

@flow
async def main_flow(list_nums: list = [1, 2, 3, 4, 5]):
    await asyncio.gather(*[sub_flow(a_number) for a_number in list_nums], return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main_flow())