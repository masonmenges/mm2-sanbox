# ---------------------------------------------------------------------------
# Automations
# Pairs with: examples/09_automations.py
#
# Use Terraform for automations that live alongside broader infrastructure
# (work pools, access control). Use the Python SDK (09_automations.py) when
# automation config lives closer to the flow definitions.
# ---------------------------------------------------------------------------

# Slack webhook block — holds the webhook URL for notifications
resource "prefect_block" "slack_webhook" {
  name         = "terraform-slack-webhook"
  type_slug    = "slack-webhook"
  workspace_id = data.prefect_workspace.this.id

  data = jsonencode({
    url = var.slack_webhook_url
  })
}

# Notify on flow run failure, crash, or timeout
resource "prefect_automation" "flow_failure_alert" {
  name         = "flow-failure-slack-alert"
  description  = "Send a Slack message when any flow run fails, crashes, or times out."
  workspace_id = data.prefect_workspace.this.id
  enabled      = true

  trigger = {
    event = {
      posture  = "Reactive"
      threshold = 1
      within    = 0

      expect = [
        "prefect.flow-run.Failed",
        "prefect.flow-run.Crashed",
        "prefect.flow-run.TimedOut",
      ]

      match = {
        "prefect.resource.id" = "prefect.flow-run.*"
      }

      for_each = ["prefect.resource.id"]
    }
  }

  actions = [
    {
      type              = "send-notification"
      block_document_id = prefect_block.slack_webhook.id
      subject           = "Prefect flow run issue"
      body              = <<-EOT
        Flow run {{ flow.name }}/{{ flow_run.name }} entered state `{{ flow_run.state.name }}`.
        Flow run URL: {{ flow_run|ui_url }}
        State message: {{ flow_run.state.message }}
      EOT
    }
  ]
}

# Event-driven automation — fire a deployment when an upstream event arrives
# Pairs with: examples/06_custom_events.py (emit_event) and prefect.yaml (event trigger)
resource "prefect_automation" "pipeline_event_trigger" {
  name         = "pipeline-downstream-trigger"
  description  = "Trigger the downstream deployment when an upstream pipeline completes."
  workspace_id = data.prefect_workspace.this.id
  enabled      = true

  trigger = {
    event = {
      posture   = "Reactive"
      threshold = 1
      within    = 0

      expect = ["myorg.pipeline.item.completed"]

      match = {
        "prefect.resource.id" = "myorg.pipeline.*"
      }

      for_each = ["prefect.resource.id"]
    }
  }

  actions = [
    {
      type            = "run-deployment"
      deployment_name = "event-emitting-flow/custom-events"
      parameters = {
        item = "{{ event.payload['item'] }}"
      }
    }
  ]
}
