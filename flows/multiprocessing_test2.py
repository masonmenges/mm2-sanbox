from prefect import flow, task
from multiprocessing import Process
from prefect.runner.storage import GitRepository


def print_func(continent='Asia'):
    print('The name of continent is : ', continent)

@task(log_prints=True)
def run_print_func():
    print("This task is to print out given continents.")
    names = ['America', 'Europe', 'Africa']
    procs = []
    proc = Process(target=print_func)  # instantiating without any argument
    procs.append(proc)
    proc.start()

    # instantiating process with arguments
    for name in names:
        # print(name)
        proc = Process(target=print_func, args=(name,))
        procs.append(proc)
        proc.start()
    # complete the processes
    for proc in procs:
        proc.join()
        proc.close()

 

@flow(name="test-multiprocessing")
def test_multiprocessing_flow():
    run_print_func()
    print("Multiprocessing works!")



if __name__ == "__main__":
    test_multiprocessing_flow()
    # test_multiprocessing_flow.from_source(
    #     source=GitRepository(
    #         url="https://github.com/masonmenges/mm2-sanbox.git",
    #         branch="main"
    #         ),
    #     entrypoint="flows/multiprocessing_test2.py:test_multiprocessing_flow"
    #     ).deploy(
    #         name="Multiprocessing Test Deployment",
    #         work_pool_name="k8s-minikube-test",
    #         image="masonm2/temprepo:withcode03132025.3",
    #         build=False,
    #         push=False
    #     )