terraform {
  required_providers {
    prefect = {
      source  = "prefecthq/prefect"
      version = "~> 2.92"
    }
  }
}

provider "prefect" {
  api_key    = var.prefect_api_key
  account_id = var.prefect_account_id
}

# ---------------------------------------------------------------------------
# Account + Workspace data sources
# ---------------------------------------------------------------------------

data "prefect_account" "this" {}

data "prefect_workspace" "this" {
  handle = var.prefect_workspace_handle
}

# ---------------------------------------------------------------------------
# Work pool + work queues
# See also: terraform/concurrency.tf for global concurrency limits
# ---------------------------------------------------------------------------

resource "prefect_work_pool" "ecs" {
  name              = "ecs-workers"
  type              = "ecs"
  workspace_id      = data.prefect_workspace.this.id
  paused            = false
  base_job_template = file("./workpools/ecs-test-pool.json")
}

resource "prefect_work_queue" "default" {
  name           = "default"
  work_pool_name = prefect_work_pool.ecs.name
  workspace_id   = data.prefect_workspace.this.id
  priority       = 4
  description    = "Default work queue"
}

resource "prefect_work_queue" "high" {
  name           = "high"
  work_pool_name = prefect_work_pool.ecs.name
  workspace_id   = data.prefect_workspace.this.id
  priority       = 1
  description    = "High priority work queue"
}

resource "prefect_work_queue" "medium" {
  name           = "medium"
  work_pool_name = prefect_work_pool.ecs.name
  workspace_id   = data.prefect_workspace.this.id
  priority       = 2
  description    = "Medium priority work queue"
}

resource "prefect_work_queue" "low" {
  name           = "low"
  work_pool_name = prefect_work_pool.ecs.name
  workspace_id   = data.prefect_workspace.this.id
  priority       = 3
  description    = "Low priority work queue"
}
