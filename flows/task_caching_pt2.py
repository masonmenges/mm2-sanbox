from prefect import flow, task
from prefect import runtime
from prefect_aws.s3 import S3Bucket
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule
from prefect.states import Failed, Completed
from prefect.cache_policies import TASK_SOURCE, INPUTS
import time

CID = "test"
FLOW_NAME ="caching_test"


LOCATION = "results-v2/"+CID+"/"+FLOW_NAME+"/"+"{flow_run.id}"+"/"
S3_BUCKET = S3Bucket.load("mm2-prefect-s3", _sync=True)
S3_BUCKET.bucket_folder = LOCATION
POLICY = INPUTS.configure(key_storage=S3_BUCKET)


@task()
def task_1():
    print("this is executing and should completed successfully")
    return True

@task(cache_policy=POLICY)
def task_2():
    if runtime.flow_run.run_count > 1:
        print("this is executing and should Complete")
        return True
    print("this is executing and should Fail")
    time.sleep(10)
    raise ValueError("task is failed")

@task()
def majo_3(param):
    print("value : {}".format(param["par"]))
    return True

@flow(log_prints=True, persist_result=True, result_storage=S3_BUCKET)
def caching_test(prev: str = None):
    p = [{"par": "first"},{"par": "second"}]
    f = task_1()
    print(f)
    g = task_2()
    print(g)
    h = majo_3.map(param=p, wait_for=[g], return_state=True)
    print(h)
    if any(state.is_failed() for state in h):
        return Failed("Mapped task failed")

    

if __name__ == "__main__":
    caching_test.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/task_caching_pt2.py:caching_test",
    ).deploy(
        name="task_caching_2",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:demo_3",
        build=False,
        push=False
    )