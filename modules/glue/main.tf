resource "aws_glue_job" "etl-spark-job" {
  name              = "${var.glue_job_name}"
  role_arn          = var.glue_role
  number_of_workers = var.spark_configurations.number_of_workers
  worker_type       = var.spark_configurations.worker_type
  max_retries       = var.spark_configurations.max_retries
  timeout           = var.spark_configurations.timeout
  glue_version      = "4.0"
  connections       = ["Snowflake connection"]
  command {
    name            = "glueetl"
    python_version  = 3
    script_location = "s3://${var.artifacts_bucket_name}/${var.script_path}"
  }
  execution_property {
    max_concurrent_runs = 2
  }
  default_arguments = var.spark_configurations.default_arguments

  tags = var.glue_tags
}