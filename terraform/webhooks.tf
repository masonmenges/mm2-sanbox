# ---------------------------------------------------------------------------
# Webhooks
# Pairs with: examples/06_custom_events.py
#
# Webhooks let external systems trigger Prefect events via HTTP POST.
# The external system only needs the webhook URL — it doesn't know anything
# about Prefect deployments. The webhook template translates the inbound
# request body into a Prefect event, which an automation then acts on.
#
# Event chain:
#   External system → POST /webhooks/{slug}
#     → Prefect event "myorg.pipeline.item.completed"
#       → automation (automations.tf) fires downstream deployment
# ---------------------------------------------------------------------------

resource "prefect_webhook" "pipeline_trigger" {
  name        = "pipeline-item-trigger"
  description = "Accepts inbound HTTP events from upstream systems and emits a Prefect event."
  workspace_id = data.prefect_workspace.this.id
  enabled     = true

  # Jinja2 template: maps inbound request body to a Prefect event
  template = <<-EOT
    {
      "event": "myorg.pipeline.item.completed",
      "resource": {
        "prefect.resource.id": "myorg.pipeline.{{ body.item_id }}"
      },
      "payload": {
        "item": "{{ body.item_id }}",
        "output_path": "{{ body.output_path }}"
      }
    }
  EOT
}

output "webhook_url_suffix" {
  description = "Append this to https://api.prefect.cloud/hooks/ to get the full webhook URL."
  value       = prefect_webhook.pipeline_trigger.slug
  sensitive   = false
}
