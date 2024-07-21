locals {  
    new_arguments = {
        "--TABLE_NAME" = local.raw_table_name
        "--RAW_BUCKET" = var.raw_bucket_name
    }

    spark_arguments = merge(var.spark_arguments, local.new_arguments)

    spark_configurations = {
        number_of_workers = 2
        worker_type = "G.1X"
        max_retries = 0
        timeout = 2880
        default_arguments = local.spark_arguments
    }

    raw_table_name = "customer_segmentation_data"
}
