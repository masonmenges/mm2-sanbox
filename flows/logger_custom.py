from prefect import flow, get_run_logger
import logging

logger = logging.getLogger("foo")
logger.setLevel(logging.INFO)

 
@flow
def bar():
  prefect_logger = get_run_logger()
  logger.info("this is foo")
  prefect_logger.info("this is the prefect logger")


