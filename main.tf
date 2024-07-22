module "s3" {
    source = "./modules/s3"

    script_path             = local.script_path
    raw_bucket_name         = local.raw_bucket_name
    artifacts_bucket_name   = local.artifacts_bucket_name
    s3_bucket_tags          = local.project_tags
    raw_table_name          = var.raw_table_name
}

module "glue" {
    source = "./modules/glue"

    glue_job_name           = local.glue_job_name
    spark_arguments         = var.spark_arguments
    spark_configurations    = local.spark_configurations
    artifacts_bucket_name   = local.artifacts_bucket_name
    script_path             = local.script_path
    glue_role               = aws_iam_role.test_role.arn
    glue_tags               = local.project_tags
}

data "aws_secretsmanager_secret" "snowflake_secret" {
    name = var.snowflake_secret_name
}