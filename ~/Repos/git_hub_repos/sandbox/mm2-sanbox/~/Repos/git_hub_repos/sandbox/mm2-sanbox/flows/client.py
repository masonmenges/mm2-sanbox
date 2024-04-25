from prefect.blocks.notifications import PagerDutyWebHook
pagerduty_webhook_block = PagerDutyWebHook.load("test-pagerduty")
pagerduty_webhook_block.notify("Hello from Prefect!")

