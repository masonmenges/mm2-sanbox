import httpx
from prefect.settings import (
    PREFECT_API_KEY,
    PREFECT_API_URL,
)

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

def get_service_accounts(client: httpx.Client) -> httpx.Response:
    return client.post(url=f"/bots/filter")

def get_account_roles(client: httpx.Client) -> httpx.Response:
    return client.post(url=f"/account_roles/filter")

def update_sa_role(client: httpx.Client,
                   service_account_id: str,
                   account_role_id: str
                   ) -> httpx.Response:
    return client.patch(
        url=f"/bots/{service_account_id}",
        json={"account_role_id": account_role_id}
    )

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
