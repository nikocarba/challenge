project = "dataengineer-challenge"

owner = "ncarballal"

raw_table_name = "customer_segmentation_data"

spark_arguments = {
    "--enable-auto-scaling"               = "true"
    "--enable-job-insights"               = "false"
    "--job-language"                      = "python"
    "--extra-jars"                        = null
    "--enable-continuous-cloudwatch-log"  = "true"
}

snowflake_secret_name = "snowflake_ncarballal"