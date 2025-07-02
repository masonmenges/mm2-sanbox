from prefect import flow, task


@task
def f(x):
    if x%2 > 1:
        raise


@flow
def test_flow():
    futures = []
    for i in range(0, 60):
        futures.append(f.submit(i))

    return futures


if __name__ == "__main__":
    test_flow()