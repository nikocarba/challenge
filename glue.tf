resource "aws_glue_job" "etl-spark-job" {
  name     = "${var.glue_job_name}"
  role_arn = "arn:aws:iam::500384448225:role/glue_god_mode"
  number_of_workers = local.spark_configurations.number_of_workers
  worker_type = local.spark_configurations.worker_type
  max_retries = local.spark_configurations.max_retries
  timeout = local.spark_configurations.timeout
  glue_version = "4.0"
  command {
    name = "glueetl"
    python_version = 3
    script_location = "s3://${var.artifacts_bucket_name}/scripts/etl.py"
  }
  execution_property {
    max_concurrent_runs = 2
  }
  default_arguments = local.spark_configurations.default_arguments
}
