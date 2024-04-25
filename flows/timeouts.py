from prefect import task, flow, get_run_logger


@task(timeout_seconds=3, retries=1)
def timeout_task():
    logger=get_run_logger()
    logger.info('Staring timeout task')
    n1 = 0
    n2 = 1
    nextn = n2
    n = 10000000
    count = 1

    while count < n:
        count += 1
        n1, n2 = n2, nextn
        nextn = n1 + n2

@flow(timeout_seconds=18)
def timeout_flow():
    timeout_task()


if __name__ == '__main__':
    timeout_flow()