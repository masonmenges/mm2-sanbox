# ---------------------------------------------------------------------------
# Access Control
# Service accounts, workspace roles, and workspace access assignments.
# ---------------------------------------------------------------------------

# Service account for CI/CD pipelines (GitHub Actions, etc.)
resource "prefect_service_account" "ci_cd" {
  name         = "ci-cd-deployer"
  account_role_name = "Member"
}

# Look up the built-in workspace roles
data "prefect_workspace_role" "developer" {
  name = "Developer"
}

data "prefect_workspace_role" "runner" {
  name = "Runner"
}

data "prefect_workspace_role" "owner" {
  name = "Owner"
}

# Grant the CI/CD service account Runner access to the workspace
# Runner role: can trigger deployments and read flow runs, but not modify infrastructure
resource "prefect_workspace_access" "ci_cd_runner" {
  accessor_type    = "SERVICE_ACCOUNT"
  accessor_id      = prefect_service_account.ci_cd.id
  workspace_id     = data.prefect_workspace.this.id
  workspace_role_id = data.prefect_workspace_role.runner.id
}

# Example: grant a team Developer access (uncomment and set team name)
# data "prefect_team" "data_engineering" {
#   name = "data-engineering"
# }
#
# resource "prefect_workspace_access" "data_eng_developer" {
#   accessor_type    = "TEAM"
#   accessor_id      = data.prefect_team.data_engineering.id
#   workspace_id     = data.prefect_workspace.this.id
#   workspace_role_id = data.prefect_workspace_role.developer.id
# }
