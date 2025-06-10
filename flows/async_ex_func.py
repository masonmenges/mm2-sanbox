import asyncio
import random

async def generate():
    value = random.random()
    await asyncio.sleep(value*10)
    return value


async def output(input:str):
    # logger = get_run_logger()
    print(f"{type(input)}")
    print(f"{input}")


async def sub_flow(input: str):
    await output(input)
    generate_output = await asyncio.gather(*[generate() for i in range(10)])
    await asyncio.gather(*[output(o) for o in generate_output])


asyncio.run(sub_flow("I'm a Function"))