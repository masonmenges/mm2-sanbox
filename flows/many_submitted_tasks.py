from prefect import flow, task
from prefect_shell import shell_run_command


@task
def f(x):
    shell_run_command.submit(
        command="sling run -r misc/sling_test.yaml"
    ).wait()

@flow
def test_flow():
    futures = []
    for i in range(0, 60):
        futures.append(f.submit(i))

    return futures


if __name__ == "__main__":
    test_flow()