import httpx
from prefect.settings import (
    PREFECT_API_KEY,
    PREFECT_API_URL,
)
from prefect import get_client, get_run_logger
from prefect.client.schemas.objects import Flow, FlowRun, State, StateType
from prefect.client.schemas.filters import (
    FlowRunFilter,
    DeploymentFilter,
    DeploymentFilterId,
    FlowRunFilterStateName,
    )
from prefect.client.schemas.sorting import FlowRunSort
from prefect.states import Cancelling

# from prefect_slack import SlackCredentials


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


def cancel_if_already_running(flow: Flow, flow_run: FlowRun, state: State):

    client = create_client(
        api_key=PREFECT_API_KEY.value(),
        base_url=PREFECT_API_URL.value()
    )

    if flow_run.deployment_id:
        filters = {
                    "sort": "ID_DESC",
                    "offset": 0,
                    "flow_runs": {
                        "state": {
                        "operator": "and_",
                        "type": {
                            "any_": [
                            "RUNNING"
                            ]
                        }
                        }
                    },
                    "deployments": {
                        "operator": "and_",
                        "id": {
                        "any_": [
                            f"{flow_run.deployment_id}"
                        ]
                        }
                    },
                    "limit": 2
                    }
        
        flow_runs_r = client.post(url="/flow_runs/filter", json=filters)
        flow_runs_r.raise_for_status()
        print(flow_runs_r.json())

        flow_runs_r.raise_for_status()
        flow_runs = flow_runs_r.json()

        print(flow_runs)
    
        if len(flow_runs) > 1:
            state=Cancelling(name="Skipped", message="A Flow run is currently running this run will be skipped").to_state_create()
            client.post(
                f"/flow_runs/{flow_run.id}/set_state",
                json=dict(state=state.dict(json_compatible=True), force=False),
            )


async def cancel_if_already_running_async(flow: Flow, flow_run: FlowRun, state: State):
    async with get_client() as client:
        if flow_run.deployment_id:
            deplyoment_filter = DeploymentFilter(
                id=DeploymentFilterId(any_=[flow_run.deployment_id])
                )
            flow_run_filter = FlowRunFilter(
                state=FlowRunFilterStateName(type=[StateType.RUNNING])
            )

            flow_runs = await client.read_flow_runs(
                    deployment_filter=deplyoment_filter,
                    flow_run_filter=flow_run_filter,
                    sort=FlowRunSort.START_TIME_DESC,
                    limit=2
                )
            
            logger = get_run_logger()

            logger.info(flow_runs)
            logger.info(len(flow_runs))
        
            if len(flow_runs) > 1:
                state=Cancelling(name="Skipped", message="A Flow run is currently running this run will be skipped")
                await client.set_flow_run_state(
                    flow_run_id=flow_run.id,
                    state=state
                )


# async def send_notification_on_failure(flow: Flow, flow_run: FlowRun, state: State):
#     params_dict = flow_run.parameters

#     slack_channel = params_dict["slack_channel"]

#     slack_block = await SlackCredentials.load("slack-creds")
#     client = slack_block.get_client()
#     response = await client.chat_postMessage(
#     channel=slack_channel,
#     text=f"""Prefect flow failed!
#     FlowRun: {flow_run.id}
#     State: {state.name}
#     State_message: {state.message}""")
#     assert response["ok"]
