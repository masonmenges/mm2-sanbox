# provider.tf / versions.tf

terraform {
  required_providers {
    prefect = {
      source = "prefecthq/prefect"
    }
  }
}

# Can be Inherited from environment variables
provider "prefect" {
  api_key = "API_KEY"
  account_id = "ACCOUNT_ID"
}

# Specify a specific workspace if necessary
resource "prefect_workspace" "sandbox" {
  name   = "sandbox-mason"
  handle = "sandbox-mason"
}


resource "prefect_work_pool" "example" {
  name              = "ecs-test-pool"
  type              = "ecs"
  workspace_id      = prefect_workspace.sandbox.id # Can also be set explicitly if necessary
  paused            = false
  base_job_template = file("./workpools/ecs-test-pool.json")
}



