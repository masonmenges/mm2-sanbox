from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
import asyncio

@flow(log_prints=True)
async def demo_flow(date: str = None):
    logger = get_run_logger()
    raise ValueError("THIS IS A TEST")
    logger.info(f"Hello World! {date}")
    logger.info(f"Config name: {configs["name"]}")



if __name__ == "__main__":
    # demo_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git",
    #         branch="main"
    #         ),
    #     entrypoint="flows/demo.py:demo_flow"
    #     ).deploy(
    #         name="Prefect_server_deployment_test_2",
    #         work_pool_name="local-server-test"
    #     )

    asyncio.run(demo_flow("2024-11-14"))