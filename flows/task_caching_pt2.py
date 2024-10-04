from prefect import flow, task
from prefect_aws.s3 import S3Bucket, AwsCredentials
from prefect.runner.storage import GitRepository
from prefect.client.schemas.schedules import CronSchedule
from prefect.states import Failed, Completed
from prefect.cache_policies import TASK_SOURCE, INPUTS
import time

CID = "test"
FLOW_NAME ="test"
SANDBOX = "test"
CLUSTER = "test-cluster"

LOCATION = "results-v2/"+CID+"/"+FLOW_NAME+"/"+"{flow_run.id}"+"/"+"{task_run.name}"+"/"
S3_BUCKET = S3Bucket.load("mm2-prefect-s3", _sync=True)

# aws_s3 = S3Bucket(bucket_name="aqfer.preprod.tmp.prefect")
# aws_s3.save(name="majo-s3", overwrite=True)
# S3_BUCKET =  S3Bucket.load("majo-s3")

S3_BUCKET.bucket_folder = LOCATION

@task()
def majo_test():
    print("this is executing and should completed successfully")
    return Completed(message="task is completed")

@task()
def majo_2():
    print("this is executing and should Faile")
    time.sleep(10)
    return Failed(message="task is failed")

@task()
def majo_3(param):
    print("value : {}".format(param["par"]))
    return Completed(message="task is completed")

@flow(log_prints=True, persist_result=True, validate_parameters=False, result_storage=S3_BUCKET)
def majo_v2(prev: str = None):
    p = [{"par": "first"},{"par": "second"}]
    f = majo_test.with_options(task_run_name="majo_test")()
    g = majo_2.with_options(task_run_name="majo_2").submit(wait_for=[f])
    g.wait()
    # h = majo_3.with_options(task_run_name="majo-[{param[par]}]").map(param=p, wait_for=[g], return_state=True)
    # if f.is_failed() or g.is_failed() or any(state.is_failed() for state in h):
    #     return Failed()
    if g.is_completed():
        return Completed()
    else:
        return Failed()