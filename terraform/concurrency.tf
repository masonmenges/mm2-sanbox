# ---------------------------------------------------------------------------
# Concurrency Limits
# Pairs with: examples/04_concurrent_tasks.py
#
# Global concurrency limits protect shared infrastructure across all deployments.
# Task run concurrency limits throttle tasks by tag within a workspace.
# ---------------------------------------------------------------------------

# Global limit — protects a shared resource (e.g. external API rate limit, GPU cluster)
# Reference in flow code:
#   from prefect.concurrency.sync import concurrency
#   with concurrency("external-api", occupy=1):
#       call_external_api()
resource "prefect_global_concurrency_limit" "external_api" {
  name         = "external-api"
  limit        = 10
  workspace_id = data.prefect_workspace.this.id
  active       = true

  # Optional: slot decay for rate limiting (slots/second)
  # slot_decay_per_second = 2.0
}

# Task tag concurrency — limits how many tasks tagged "gpu" run simultaneously
# Tag tasks in flow code:
#   @task(tags=["gpu"])
#   def train_model(): ...
resource "prefect_task_run_concurrency_limit" "gpu_tasks" {
  tag          = "gpu"
  concurrency_limit = 4
  workspace_id = data.prefect_workspace.this.id
}
