from prefect import flow, task

@flow(log_prints=True)
def persist_test():
    passing_task()
    failing_task()

@task(persist_result=True)
def passing_task():
    print("This task should be skipped on retry")
    return 42

@task(persist_result=True)
def failing_task():
    raise ValueError("This task failed")

if __name__=="__main__":
    persist_test.serve()