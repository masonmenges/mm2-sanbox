# ---------------------------------------------------------------------------
# Prefect provider variables
# Set via environment variables before running terraform apply:
#   export TF_VAR_prefect_api_key=$PREFECT_API_KEY
#   export TF_VAR_prefect_account_id=$PREFECT_ACCOUNT_ID
#   export TF_VAR_prefect_workspace_handle=your-workspace-handle
# ---------------------------------------------------------------------------

variable "prefect_api_key" {
  description = "Prefect Cloud API key. Use a service account key for CI/CD."
  type        = string
  sensitive   = true
}

variable "prefect_account_id" {
  description = "Prefect Cloud account UUID."
  type        = string
}

variable "prefect_workspace_handle" {
  description = "Handle (slug) of the target workspace, e.g. 'my-team-prod'."
  type        = string
}

variable "slack_webhook_url" {
  description = "Slack incoming webhook URL for flow failure notifications."
  type        = string
  sensitive   = true
  default     = ""
}
