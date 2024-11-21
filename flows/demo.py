from prefect import flow, task, get_run_logger
from prefect.runner.storage import GitRepository  
import asyncio

@flow(log_prints=True)
async def demo_flow(date: str = None):
    logger = get_run_logger()
    logger.info(f"Hello World! {date}")



if __name__ == "__main__":
    # demo_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git",
    #         branch="main"
    #         ),
    #     entrypoint="flows/demo.py:demo_flow"
    #     ).deploy(
    #         name="Prefect_managed_deployment_test",
    #         work_pool_name="mm2-test"
    #     )

    asyncio.run(demo_flow("2024-11-14"))