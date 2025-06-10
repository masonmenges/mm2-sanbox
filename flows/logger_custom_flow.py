import logger_custom as foo

from prefect import flow, get_run_logger

@flow
def logging_test_flow():
    prefect_logger = get_run_logger()
    foo.bar()
    prefect_logger.info("This is the prefect logger")
 


if __name__ == "__main__":
    logging_test_flow()