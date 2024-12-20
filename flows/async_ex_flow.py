from prefect import flow, task, get_run_logger
import random, asyncio
from time import sleep

@task
async def generate():
    value = random.random()
    await asyncio.sleep(value*10)
    return value

@task
def output(input:str):
    logger = get_run_logger()
    logger.info(f"{type(input)}")
    logger.info(f"{input}")

@flow
async def sub_flow(input: str):
    output(input)
    data_futures=[generate.submit() for i in range(10)]
    for data in data_futures:
        output.submit(data)
        
asyncio.run(sub_flow("I'm a Flow"))