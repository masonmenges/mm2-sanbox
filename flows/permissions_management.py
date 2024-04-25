import httpx
from prefect.settings import (
    PREFECT_API_KEY,
    PREFECT_API_URL,
)
from prefect import get_client


def create_client(
        api_key: str,
        base_url: str,
        httpx_settings: dict = None, 
        account_client: bool = False
        ) -> httpx.Client:

    if account_client:
        base_url = base_url.split("/workspaces")[0]

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
    return client.post(url=f"/bots/filter")

def get_account_roles(client: httpx.Client) -> httpx.Response:
    return client.post(url=f"/account_roles/filter")


def create_acl(client: httpx.Client, deployment_id: str, acls: dict) -> httpx.Response:
    return client.put(
        url=f"/deployments/{deployment_id}/access",
        json=acls
    )

def update_sa_role(client: httpx.Client,
                   service_account_id: str,
                   account_role_id: str
                   ) -> httpx.Response:
    return client.patch(
        url=f"/bots/{service_account_id}",
        json={"account_role_id": account_role_id}
    )

def update_deployment_acls():
    prefect_client = create_client(
        api_key=PREFECT_API_KEY.value(),
        base_url=PREFECT_API_URL.value(),
        account_client=True
        )

    r_deployments = get_deployments(prefect_client)

    r_memberships = get_service_accounts(prefect_client)
    deployments = r_deployments.json()
    memberships = r_memberships.json()
    print(memberships)

    for membership in memberships:
        if membership["name"] == "test-acl":
            sa_actor_id = membership["actor_id"]

            r_acl = create_acl(
                client=prefect_client,
                deployment_id=deployments[0]["id"],
                acls={
                    "access_control": {
                        "manage_actor_ids": [f"{sa_actor_id}"],
                        "run_actor_ids": [],
                        "view_actor_ids": [],
                        "manage_team_ids": [],
                        "run_team_ids": [],
                        "view_team_ids": []
                    }
                    }
            )
            print(r_acl.status_code)


def update_bot_role(role_name: str, service_account_name: str):
    prefect_client = create_client(
        api_key=PREFECT_API_KEY.value(),
        base_url=PREFECT_API_URL.value(),
        account_client=True
        )
    
    r_memberships = get_service_accounts(prefect_client)
    r_roles = get_account_roles(client=prefect_client)
    memberships = r_memberships.json()

    roles = r_roles.json()

    for role in roles:
        if role["name"] == role_name:
            role_id = role["id"]


    for membership in memberships:
        if membership["name"] == service_account_name:
            print("updating service account role")
            sa_id = membership["id"]
            update_r = update_sa_role(
                client=prefect_client,
                service_account_id=sa_id,
                account_role_id=role_id
            )
            update_r.raise_for_status()
            print(update_r.status_code)


if __name__ == "__main__":
    update_bot_role(
        role_name="Admin",
        service_account_name="test-acl"
    )
