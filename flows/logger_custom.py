import logging

logger = logging.getLogger("foo")
logger.setLevel(logging.INFO)

 
def bar():
  logger.info("this is foo")


