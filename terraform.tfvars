raw_bucket_name = "raw-bucket-test-terraform-ncarballal"

artifacts_bucket_name = "artifacts-bucket-test-terraform-ncarballal"

glue_job_name = "raw_data_to_snowflake"

spark_arguments = {
    "--enable-auto-scaling" = "true"
    "--enable-job-insights" = "false"
    "--job-language"        = "python"
    "--extra-jars"          = null
    "--TABLE_NAME"          = "customer_segmentation_data"
}
