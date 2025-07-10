import os 

from random import randint

def get_num_workers_value():
    num_workers = randint(1, 8)

    os.environ["num_workers"] = str(num_workers)

    print(os.environ["num_workers"])