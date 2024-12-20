from prefect import get_client
import asyncio

async def update_deployment_pull_steps(updated_pull_steps: list[dict], dep_name: str):
    client = get_client()

    d = await client.read_deployment_by_name(name=dep_name)

    d.pull_steps = updated_pull_steps

    d_json = d.model_dump()

    invalid_keys = ["id",
                    "created",
                    "updated",
                    "created_by",
                    "updated_by",
                    "global_concurrency_limit",
                    "last_polled",
                    "work_queue_id",
                    "status"
                    ]
    
    for key in invalid_keys:
        del d_json[key]

    await client.create_deployment(**d_json)

if __name__ == "__main__":
    updated_pull_steps = [{"prefect.deployments.steps.git_clone":{"branch":None,"repository":"https://github.com/masonmenges/mm2-sanbox.git"}}]
    dep_name = "demo-flow/ecs-demo-test"

    asyncio.run(update_deployment_pull_steps(updated_pull_steps=updated_pull_steps, dep_name=dep_name))

