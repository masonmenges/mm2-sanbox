from prefect import flow, task
import asyncio
import time 
import random

from prefect import get_client

# def on_running_function(flow, flow_run, state):
#     if flow_run.run_count <= 0:
#         print(f"I am an on_running function! The flow is currently in state {state}")
#     else:
#         print("skipping on_running function")

@task
async def compute_task():
    async with get_client() as client:
        dep = await client.read_deployment("799c5f9f-7e84-4257-8f79-493b494ba244")
        print(dep.name)

@task
async def secondary_task():
    print("I'm a second task!")
    time.sleep(5)

@flow(retries=2)
async def demo_flow():
    await compute_task()

    number = random.randint(1, 10)

    if number >= 5:
        await secondary_task()

    return True


if __name__ == "__main__":
    state = asyncio.run(demo_flow())

