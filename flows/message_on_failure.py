import asyncio
from prefect import flow
from prefect.states import Crashed
from prefect.client.schemas.objects import Flow, FlowRun, State

from prefect_slack import SlackCredentials


async def send_notification_on_failure(flow: Flow, flow_run: FlowRun, state: State):
    params_dict = flow_run.parameters

    slack_channel = params_dict["slack_channel"]

    slack_block = await SlackCredentials.load("slack-creds")
    client = slack_block.get_client()
    response = await client.chat_postMessage(
    channel=slack_channel,
    text=f"""Prefect flow failed!
    FlowRun: {flow_run.id}
    State: {state.name}
    State_message: {state.message}""")
    assert response["ok"]


@flow(on_failure=[send_notification_on_failure])
async def failed_flow(slack_channel: str = "#test"):
    raise ValueError("This flow failed")

@flow(on_crashed=[send_notification_on_failure])
async def crashed_flow(slack_channel: str = "#test"):
    return Crashed(message="This flow crashed")

if __name__ == "__main__":
    # asyncio.run(failed_flow())
    asyncio.run(crashed_flow())