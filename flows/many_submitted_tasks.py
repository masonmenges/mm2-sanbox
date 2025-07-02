from prefect import flow, task


@task
def f(x):
    if x > 10:
        raise


@flow
def test_flow():
    futures = []
    for i in range(0, 15):
        futures.append(f.submit(i))

    return futures


if __name__ == "__main__":
    test_flow()