from prefect import task, flow

from state_change_hooks import task_params_on_failure
import time

@task(on_failure=[task_params_on_failure])
def fail_task():
    time.sleep(600)


@flow
def fail_flow():
    fail_task()

if __name__ == "__main__":
    fail_flow.from_source(
        source="/Users/masonmenges/Repos/git_hub_repos/mm2-sanbox/flows",
        entrypoint="task_sch.py:fail_flow"
    ).deploy(
        name="task_sch_failure_on_cancel",
        work_pool_name="local-cloud-test",
    )