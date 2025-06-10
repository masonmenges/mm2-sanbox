import datetime, pytz

from prefect import flow, get_run_logger
from prefect.runner.storage import GitRepository


@flow(retries=2, log_prints=True)
def demo_windows_flow():
    logger = get_run_logger()
    logger.info("This is a Windows Flow")

    time = datetime.datetime.now().astimezone(pytz.timezone(("US/Mountain")))

    with open("C:\\Users\\track\\Desktop\\testdoc.txt", "a") as f:
        f.write(f"Ran at {time}\n")


if __name__ == "__main__":
    # state = asyncio.run(demo_flow())
    demo_windows_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
        entrypoint="flows/demo_windows.py:demo_windows_flow",
    ).deploy(
        name="testing_git_windows",
        work_pool_name="windows_local_pool"
    )
