from uuid import UUID
from prefect import get_client
from prefect.client.schemas.objects import Flow, FlowRun, State, StateType
from prefect.client.schemas.filters import (
    FlowRunFilter,
    DeploymentFilter,
    DeploymentFilterId,
    FlowRunFilterStateName,
    )
from prefect.client.schemas.sorting import FlowRunSort
from prefect.states import Cancelled


async def cancel_if_already_running(flow: Flow, flow_run: FlowRun, state: State):
    async with get_client() as client:
        #for testing
        flow_run.deployment_id = UUID("799c5f9f-7e84-4257-8f79-493b494ba244")
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
        
            if len(flow_runs) > 1:
                state=Cancelled(name="Skipped", message="A Flow run is currently running this run will be skipped")
                await client.set_flow_run_state(
                    flow_run_id=flow_run.id,
                    state=state
                )