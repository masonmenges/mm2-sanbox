import datetime, pytz

from prefect import flow, get_run_logger
from prefect.runner.storage import GitRepository


@flow(retries=2, log_prints=True)
def demo_windows_flow():
    logger = get_run_logger()
    logger.info("This is a Windows Flow")

    time = datetime.datetime.now().astimezone(pytz.timezone(("US/Mountain")))

    with open("C:\\Users\\track\\Desktop\\testdoc.txt", "a") as f:
        f.write(f"Ran at {time}")


if __name__ == "__main__":
    # state = asyncio.run(demo_flow())
    # demo_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git"
    #         ),
    #     entrypoint="flows/demo_windows.py:demo_flow",
    # ).deploy(
    #     name="local_windows_test",
    #     work_pool_name="windows_local_pool",
    #     job_variables={
    #         "pip_packages": ["pandas", "sqlalchemy", "prefect-snowflake", "prefect-slack"]
    #     }
    # )
    demo_windows_flow()
