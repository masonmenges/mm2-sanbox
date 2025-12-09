import csv, random, duckdb, os

from prefect import flow, task
from prefect_shell import shell_run_command


def generate_random_row(col, i):
    a = []
    l = [i]
    for j in range(col):
        l.append(random.random())
    a.append(l)
    return a

@task
def gen_csv(n, rows = 5000, columns = 26, print_after_rows = 500):
    f_name = f'sample{n}.csv'
    f = open(f_name, 'w')
    w = csv.writer(f, lineterminator='\n')
    for i in range(rows):
        if i % print_after_rows == 0:
            print(".", end="", flush=True)
        w.writerows(generate_random_row(columns, i))
    f.close()

    return f_name

@task
def create_duckdb(n):
    db_name = f"sample{n}.db"
    print(db_name)
    conn = duckdb.connect(db_name)
    conn.sql("CREATE SCHEMA test")
    os.environ.setdefault(f"duckdb_{n}", f"duckdb://{db_name}")
    return f"duckdb_{n}"


@task
def f(csv_file_name, duck_db):

    cmd = f"sling run --src-stream 'file://{csv_file_name}' --tgt-conn {duck_db} --tgt-object 'test' --mode full-refresh"

    shell_run_command.with_options(timeout_seconds=600).submit(
        command=cmd
    ).wait()

@flow(name="ECS_flows")
def test_flow():
    futures = []
    for i in range(0, 10):
        f_name = gen_csv.submit(i)
        db_name = create_duckdb.submit(i)
        futures.append(f.submit(f_name, db_name))

    return futures

if __name__ == "__main__":
    test_flow()