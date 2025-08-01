import asyncio

from random import random, uniform
from prefect import flow, task, get_run_logger
from prefect.futures import wait


@task
async def run_loader(config):
    logger = get_run_logger()
    try:
        # start = 0
        n = 1
        while True:
            await asyncio.sleep(5)

    except asyncio.CancelledError:
        logger.warning(f"got cancellation signal!")
        raise

    except Exception as ex:
        logger.error(f" got unexpected exception: {ex}")
        raise


@flow(log_prints=True)
async def sf_loader():
    logger = get_run_logger()
    # configs = [load_yaml_config("src/configs.yaml", env=ENV)]
    tasks = []
    results = []

    for cfg in range(0, 10):
        # get_all_secrets(cfg['sec_cfgs']['secrets'])
        task = run_loader.submit(cfg)
        tasks.append(task)
    logger.info(f"All tasks submitted!")

    wait(tasks)    

    try:
        for task in tasks:
            results.append(task.result())
    except asyncio.CancelledError:
        logger.warning(f"main flow got manual cancellation! Notifying all tasks...")
        for task in tasks:

            task.cancel()
        raise
    except Exception as ex:
        logger.error(f"main flow unexpected failed: {ex}")
        raise

if __name__ == "__main__":
    sf_loader.serve()