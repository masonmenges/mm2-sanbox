import httpx
from prefect.settings import (
    PREFECT_API_KEY,
    PREFECT_API_URL,
)

def create_client(api_key: str, base_url: str, httpx_settings: dict = None) -> httpx.Client:

    httpx_settings = {
        "headers": {}
    }
    httpx_settings["headers"].setdefault("Authorization", f"Bearer {api_key}")
    httpx_settings.setdefault("base_url", base_url)

    return httpx.Client(**httpx_settings)    


def get_deployments(client: httpx.Client, filters: dict = None) -> httpx.Response:

    # Filter by tag or tags, you can also specify an operator
    # defaults to "and_" 
    filters = {
        "deployments": {
            "operator": "or_",
            "tags": {
                "all_": ["Testing"]
            }
        }
    }

    return client.post(url="/deployments/filter", json=filters)

def get_service_accounts(client: httpx.Client) -> httpx.Response:
    return client.post(url="https://api.prefect.cloud/api/accounts/9b649228-0419-40e1-9e0d-44954b5c0ab6/bots/filter")


def create_acl(client: httpx.Client, deployment_id: str, acls: dict) -> httpx.Response:
    return client.put(
        url=f"/deployments/{deployment_id}/access",
        json=acls
    )



test = create_client(
    api_key=PREFECT_API_KEY.value(),
    base_url=PREFECT_API_URL.value(),
    )

r_deployments = get_deployments(test)

r_memberships = get_service_accounts(test)
deployments = r_deployments.json()
memberships = r_memberships.json()
print(memberships)

for membership in memberships:
    if membership["name"] == "test-acl":
        sa_id = membership["actor_id"]

        print(sa_id)

        r_acl = create_acl(
            client=test,
            deployment_id=deployments[0]["id"],
            acls={
                "access_control": {
                    "manage_actor_ids": [f"{sa_id}"],
                    "run_actor_ids": [],
                    "view_actor_ids": [],
                    "manage_team_ids": [],
                    "run_team_ids": [],
                    "view_team_ids": []
                }
                }
        )
        print(r_acl.status_code)
        print(r_acl.json()) 



