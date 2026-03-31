# ---------------------------------------------------------------------------
# Blocks
# Pairs with: examples/03_task_caching.py
#
# Prefect Blocks store configuration and credentials that flows can load at
# runtime. Managing blocks via Terraform ensures they exist before deployments
# run and their configuration is version-controlled alongside infrastructure.
# ---------------------------------------------------------------------------

# S3 bucket block for task result storage (used by 03_task_caching.py)
# The flow loads this block by name:
#   S3Bucket.load(os.getenv("S3_RESULT_BUCKET", "task-result-storage"))
resource "prefect_block" "s3_result_storage" {
  name         = "task-result-storage"
  type_slug    = "s3-bucket"
  workspace_id = data.prefect_workspace.this.id

  data = jsonencode({
    bucket_name   = "your-prefect-results-bucket"
    bucket_folder = "task-cache"
    # credentials: omit to use IAM role attached to the worker,
    # or reference an aws-credentials block:
    # aws_credentials = { "$ref": { "block_document_id": "<uuid>" } }
  })
}
