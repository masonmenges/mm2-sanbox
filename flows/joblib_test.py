from prefect import flow, task
from time import sleep
from joblib import Parallel, delayed

import os


# This is the function we're going to parallelize
def slow_square(n):
    print(f"Computing square of {n}.. {os.getpid()}")
    sleep(10)  # Simulate a slow function
    return n**2


@task
def heavyduty_fn(inputs):    
    # Use joblib to parallelize the slow_square function
    results = Parallel(n_jobs=-1, backend="multiprocessing")(delayed(slow_square)(i) for i in inputs)

    return results


@flow
def main():
  inputs = range(100)
  r = heavyduty_fn(inputs)
#   results = Parallel(n_jobs=-1, backend="multiprocessing")(delayed(slow_square)(i) for i in inputs)

if __name__ == "__main__":
    main()