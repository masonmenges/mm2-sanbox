from prefect import task
import time

@task
def background_task():
    print("backgrounded process")
    time.sleep(10)

if __name__ == "__main__":
    background_task.serve()