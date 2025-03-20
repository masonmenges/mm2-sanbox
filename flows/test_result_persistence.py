from prefect import flow, task
from prefect.runner.storage import GitRepository
from prefect_aws import S3Bucket, AwsCredentials

aws_creds = AwsCredentials.load("mm2-se-dev", _sync=True)

result_storage = S3Bucket(
    bucket_name="mm2-results",
    bucket_folder="Prefect3",
    credentials=aws_creds
)
result_storage.save(name="mm2-results3", overwrite=True, _sync=True)

@flow(
        log_prints=True,
        result_storage=result_storage,
        persist_result=True,
        retries=1
        )
def persist_test():
    success_task = passing_task()
    return success_task

@task(persist_result=True
      )
def passing_task(some_param: int = 42, parent_run_id=None):
    print("This task should be skipped on retry")
    return 42

if __name__=="__main__":
    # persist_test()
    persist_test.from_source(
            source=GitRepository(
                url="https://github.com/masonmenges/mm2-sanbox.git"
                ),
            entrypoint="flows/test_result_persistence.py:persist_test",
        ).deploy(
        name="result_persistence-test_3.x",
        work_pool_name="k8s-minikube-test",
        image="masonm2/temprepo:withcode03132025.2",
        build=False,
        push=False
        )