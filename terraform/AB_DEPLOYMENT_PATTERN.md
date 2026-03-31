# A/B Deployment Pattern in Prefect with Automated Failover

This guide explains how to create an A/B deployment pattern with Prefect, where you have identical deployments running in two separate regions with automated failover using Prefect automations.

## Overview

An A/B deployment pattern with automated failover involves:
- Two work pools (one per region)
- Two deployments of the same flow (one per region)
- Prefect automations that monitor for failures and trigger failover
- Work queues to route traffic to specific regions
- Agents/workers running in each region

## Architecture

```
Flow
├── Deployment A (Region A) → Work Pool A → Workers in Region A
│   └── Automation: Monitor for failures → Trigger Deployment B
│
└── Deployment B (Region B) → Work Pool B → Workers in Region B
    └── Automation: Monitor for failures → Trigger Deployment A
```

## Step 1: Create Work Pools for Each Region

```hcl
# Work Pool for Region A (e.g., us-east-1)
resource "prefect_work_pool" "region_a" {
  name              = "ecs-us-east-1"
  type              = "ecs"
  workspace_id      = data.prefect_workspace.my_workspace.id
  paused            = false
  base_job_template = file("./workpools/us-east-1-pool.json")
}

# Work Pool for Region B (e.g., us-west-2)
resource "prefect_work_pool" "region_b" {
  name              = "ecs-us-west-2"
  type              = "ecs"
  workspace_id      = data.prefect_workspace.my_workspace.id
  paused            = false
  base_job_template = file("./workpools/us-west-2-pool.json")
}
```

## Step 2: Create Deployments for Each Region

### Using Python

```python
from prefect import flow
from prefect.deployments import Deployment

@flow(log_prints=True)
def my_flow():
    print("Running flow")
    # Your flow logic here

# Deployment for Region A (Primary)
deployment_a = Deployment.build_from_flow(
    flow=my_flow,
    name="my-flow-region-a",
    work_pool_name="ecs-us-east-1",
    tags=["region-a", "us-east-1", "primary"],
)
deployment_a.apply()

# Deployment for Region B (Backup)
deployment_b = Deployment.build_from_flow(
    flow=my_flow,
    name="my-flow-region-b",
    work_pool_name="ecs-us-west-2",
    tags=["region-b", "us-west-2", "backup"],
)
deployment_b.apply()
```

## Step 3: Create Automations for Automatic Failover

### Automation 1: Failover from Region A to Region B on Failure

This automation monitors Region A deployments and triggers Region B if failures are detected:

```python
from prefect.automations import Automation
from prefect.events.schemas.automations import EventTrigger, Posture
from prefect.events.actions import RunDeployment

# Create automation to failover from A to B
automation_a_to_b = Automation(
    name="Failover: Region A → Region B",
    description="Trigger Region B deployment when Region A fails",
    trigger=EventTrigger(
        expect={"prefect.flow-run.Failed"},
        match={
            "prefect.resource.name": "my-flow-region-a"
        },
        posture=Posture.Reactive,
        threshold=2,  # Trigger after 2 failures
        within=300,   # Within 5 minutes
    ),
    actions=[
        RunDeployment(
            source="selected",
            deployment_id="<deployment-b-id>",  # Replace with actual ID
            parameters={},
        )
    ],
    enabled=True,
)
automation_a_to_b.create()
```

### Automation 2: Failover from Region B to Region A on Failure

This automation monitors Region B deployments and triggers Region A if failures are detected:

```python
# Create automation to failover from B to A
automation_b_to_a = Automation(
    name="Failover: Region B → Region A",
    description="Trigger Region A deployment when Region B fails",
    trigger=EventTrigger(
        expect={"prefect.flow-run.Failed"},
        match={
            "prefect.resource.name": "my-flow-region-b"
        },
        posture=Posture.Reactive,
        threshold=2,  # Trigger after 2 failures
        within=300,   # Within 5 minutes
    ),
    actions=[
        RunDeployment(
            source="selected",
            deployment_id="<deployment-a-id>",  # Replace with actual ID
            parameters={},
        )
    ],
    enabled=True,
)
automation_b_to_a.create()
```

### Getting Deployment IDs

```python
from prefect import get_client

async def get_deployment_ids():
    async with get_client() as client:
        # Get deployment A ID
        deployment_a = await client.read_deployment_by_name(
            "my-flow/my-flow-region-a"
        )
        print(f"Deployment A ID: {deployment_a.id}")

        # Get deployment B ID
        deployment_b = await client.read_deployment_by_name(
            "my-flow/my-flow-region-b"
        )
        print(f"Deployment B ID: {deployment_b.id}")

# Run this to get your deployment IDs
import asyncio
asyncio.run(get_deployment_ids())
```

## Step 4: Advanced Automation Patterns

### Pattern 1: Cascade Failover with Alerts

Failover to backup region and send notifications:

```python
from prefect.events.actions import RunDeployment, SendNotification

automation_with_alert = Automation(
    name="Failover with Alert: Region A → Region B",
    trigger=EventTrigger(
        expect={"prefect.flow-run.Failed"},
        match={
            "prefect.resource.name": "my-flow-region-a"
        },
        posture=Posture.Reactive,
        threshold=2,
        within=300,
    ),
    actions=[
        SendNotification(
            block_document_id="<slack-webhook-id>",
            subject="Failover Alert: Switching to Region B",
            body="Region A experienced failures. Triggering Region B deployment.",
        ),
        RunDeployment(
            source="selected",
            deployment_id="<deployment-b-id>",
        )
    ],
    enabled=True,
)
```

### Pattern 2: Worker Health Monitoring

Trigger failover if workers become unhealthy:

```python
automation_worker_health = Automation(
    name="Failover on Worker Unhealthy",
    trigger=EventTrigger(
        expect={"prefect.work-pool.not-ready"},
        match={
            "prefect.resource.name": "ecs-us-east-1"
        },
        posture=Posture.Reactive,
        threshold=1,
        within=60,
    ),
    actions=[
        RunDeployment(
            source="selected",
            deployment_id="<deployment-b-id>",
        )
    ],
    enabled=True,
)
```

### Pattern 3: Scheduled Health Checks

Create a monitoring flow that triggers failover based on custom health checks:

```python
from prefect import flow, get_run_logger
from prefect.deployments import run_deployment

@flow
def health_check_and_route():
    logger = get_run_logger()

    # Custom health check logic
    region_a_healthy = check_region_health("us-east-1")
    region_b_healthy = check_region_health("us-west-2")

    if not region_a_healthy and region_b_healthy:
        logger.warning("Region A unhealthy, routing to Region B")
        run_deployment("my-flow/my-flow-region-b")
    elif region_a_healthy:
        logger.info("Region A healthy, using primary deployment")
        run_deployment("my-flow/my-flow-region-a")
    else:
        logger.error("Both regions unhealthy!")
        raise Exception("No healthy regions available")

def check_region_health(region: str) -> bool:
    # Implement your health check logic
    # Check worker status, resource availability, etc.
    return True
```

## Step 5: Run Workers in Each Region

Start workers in each region that poll their respective work pools:

```bash
# In Region A (us-east-1)
prefect worker start --pool ecs-us-east-1

# In Region B (us-west-2)
prefect worker start --pool ecs-us-west-2
```

## Monitoring Your A/B Setup

### View Automation Runs

```python
from prefect import get_client

async def check_automation_activity():
    async with get_client() as client:
        automations = await client.read_automations()

        for automation in automations:
            if "Failover" in automation.name:
                print(f"Automation: {automation.name}")
                print(f"Enabled: {automation.enabled}")
                print(f"Trigger count: {automation.trigger_count}")
```

### Track Regional Performance

```python
from prefect import get_client
from datetime import datetime, timedelta

async def regional_performance():
    async with get_client() as client:
        last_hour = datetime.now() - timedelta(hours=1)

        # Region A stats
        region_a_runs = await client.read_flow_runs(
            deployment_filter={"tags": {"all_": ["region-a"]}},
            flow_run_filter={"start_time": {"after_": last_hour}}
        )

        # Region B stats
        region_b_runs = await client.read_flow_runs(
            deployment_filter={"tags": {"all_": ["region-b"]}},
            flow_run_filter={"start_time": {"after_": last_hour}}
        )

        print(f"Region A runs: {len(region_a_runs)}")
        print(f"Region B runs: {len(region_b_runs)}")
```

## Benefits

1. **Automatic Failover**: No manual intervention needed when failures occur
2. **High Availability**: System self-heals by switching regions
3. **Configurable Thresholds**: Set custom failure thresholds before triggering failover
4. **Observable**: Track automation triggers and regional performance
5. **Flexible**: Combine with notifications, custom health checks, and more

## Best Practices

1. **Set Appropriate Thresholds**: Don't trigger failover on single transient failures
2. **Monitor Both Regions**: Ensure workers are running and healthy in both regions
3. **Test Failover**: Regularly test your automation triggers
4. **Alert on Failover**: Always send notifications when failover occurs
5. **Prevent Ping-Pong**: Add cooldown periods to avoid rapid back-and-forth switching
6. **Keep Deployments Synced**: Ensure both deployments use the same code version
