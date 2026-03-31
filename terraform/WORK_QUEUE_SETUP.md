# Managing Prefect Work Pool and Default Work Queue with Terraform

When creating a Prefect work pool, Prefect automatically creates a "default" work queue. Follow these steps to manage it with Terraform from the start.

## Steps

### 1. Define your work pool and default work queue resource

```hcl
resource "prefect_work_pool" "my_pool" {
  name              = "my-work-pool"
  type              = "ecs"
  workspace_id      = data.prefect_workspace.my_workspace.id
  paused            = false
  base_job_template = file("./workpools/my-pool.json")
}

# Define the default work queue that Prefect will create automatically
resource "prefect_work_queue" "default" {
  name              = "default"
  work_pool_name    = prefect_work_pool.my_pool.name
  workspace_id      = data.prefect_workspace.my_workspace.id
  priority          = 10
  description       = "Default work queue"
}
```

### 2. Create the work pool (but not the default queue yet)

```bash
# This will create the work pool and attempt to create the default queue
# The default queue creation will fail because Prefect already created one
terraform apply
```

The apply will succeed for the work pool but fail for the default work queue resource because it already exists.

### 3. Import the auto-created default work queue

Get your workspace ID:
```bash
terraform state show data.prefect_workspace.my_workspace
```

Import the default work queue using the format: `work_pool_name,work_queue_name,workspace_id`

```bash
terraform import prefect_work_queue.default my-work-pool,default,<workspace-id>
```

### 4. Apply again to sync configuration

```bash
terraform apply
```

This will update the default work queue with your desired configuration (priority, description, etc.).

### 5. Add custom work queues (optional)

```hcl
resource "prefect_work_queue" "high_priority" {
  name              = "high-priority"
  work_pool_name    = prefect_work_pool.my_pool.name
  workspace_id      = data.prefect_workspace.my_workspace.id
  priority          = 1
  description       = "High priority work queue"
}

resource "prefect_work_queue" "low_priority" {
  name              = "low-priority"
  work_pool_name    = prefect_work_pool.my_pool.name
  workspace_id      = data.prefect_workspace.my_workspace.id
  priority          = 5
  description       = "Low priority work queue"
}
```

## Priority Numbers

Lower numbers = higher priority. Recommended structure:
- Priority 1: Critical/urgent tasks
- Priority 2-5: High to medium priority
- Priority 6-9: Low priority
- Priority 10+: Default/background tasks
