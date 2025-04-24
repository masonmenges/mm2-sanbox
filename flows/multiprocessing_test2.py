from prefect import flow, task
from prefect.runner.storage import GitRepository

import multiprocessing

from multiprocessing import Queue

import gzip

 
@flow
def test_multiprocessing_flow(buf = """I'm a random test",
        The quick brown fox jumps over the lazy dog,
        Lorem ipsum dolor sit amet,
        Python is awesome!,
        Testing multiprocessing gzip compression,
        Another random string for testing purposes,
        Encoding and compressing this text,
        The weather is nice today,
        Random test string number nine,
        Last but not least, the final test string""".encode(), procs = 10):

    queue = Queue()

    workers = []

    print(f"Starting {procs} gzip jobs.")

    for num in range(procs):

        # worker = Process(target=gzip_worker, args=(buf, num, procs, queue))

        ctx = multiprocessing.get_context("spawn")

        worker = ctx.Process(target=gzip_worker, args=(buf, num, procs, queue))

        worker.start()

        workers.append(worker)

    print("gzip jobs submitted. Collecting results.")

    parts = []

    for _ in workers:

        parts.append(queue.get())

    for worker in workers:

        worker.join()

        if worker.exitcode != 0:

            raise RuntimeError(f'A worker returned {worker.exitcode} exit code')

    parts.sort(key=lambda x: x[0])

    print("Return zipped results as a list.")

    return [part[1] for part in parts]

   
def gzip_worker(buf, num, procs, queue):

    size = len(buf)

    start = int(size / procs * num)

    end = int(size / procs * (num + 1))

    out = gzip.compress(buf[start:end])

    queue.put((num, out))


if __name__ == "__main__":
    test_multiprocessing_flow.from_source(
        source=GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git",
            branch="main"
            ),
        entrypoint="flows/multiprocessing_test2.py:test_multiprocessing_flow"
        ).deploy(
            name="Multiprocessing Test Deployment",
            work_pool_name="k8s-minikube-test",
            image="masonm2/temprepo:withcode03132025.3",
            build=False,
            push=False
        )