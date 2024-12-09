from prefect import flow, task
from prefect.runner.storage import GitRepository
from prefect.deployments import run_deployment
import numpy as np
import uuid
import time
import asyncio

@flow
async def parent_flow():

    companies_list = []
    for _ in range(100):
        companies_list.append(uuid.uuid4())

    company_batches = np.array_split(companies_list, 10)

    for batch in company_batches:
        processing_companies = [run_deployment(name="child_flow/process_company", parameters={"company_id": id})
         for id in batch]
        
        await asyncio.gather(*processing_companies)

@flow
def child_flow(company_id: uuid.UUID):
    print(f"process_executed on {company_id}")
    time.sleep(10)

if __name__ == "__main__":
    parent_flow.from_source(GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
    entrypoint="flows/parent_child_pattern.py:parent_flow",
    ).deploy(
    name="parent_demo",
    work_pool_name="local-cloud-test",
    version="parent_demo:0.0.2",
    )

    child_flow.from_source(GitRepository(
            url="https://github.com/masonmenges/mm2-sanbox.git"
            ),
    entrypoint="flows/parent_child_pattern.py:child_flow",
    ).deploy(
    name="process_company", 
    work_pool_name="local-cloud-test",
    version="child_demo:0.0.2",
    )