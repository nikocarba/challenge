resource "aws_s3_bucket" "raw-bucket" {
    bucket = var.raw_bucket_name
    tags = var.s3_bucket_tags
}

resource "aws_s3_bucket" "artifacts-bucket" {
    bucket = var.artifacts_bucket_name
    tags = var.s3_bucket_tags
}

resource "aws_s3_object" "raw-data" {
  bucket = aws_s3_bucket.raw-bucket.id
  key    = "${var.raw_table_name}.csv"
  source = "data/${var.raw_table_name}.csv"

  etag = filemd5("data/${var.raw_table_name}.csv")
}

resource "aws_s3_object" "glue-script" {
  bucket = aws_s3_bucket.artifacts-bucket.id
  key    = var.script_path
  source = "./scripts/glue_script.py"

  etag = filemd5("./scripts/glue_script.py")
}

resource "aws_s3_object" "etl-configs" {
  bucket = aws_s3_bucket.artifacts-bucket.id
  key    = "etl-configs/customer_segmentation_data.json"
  source = "./etl-configs/customer_segmentation_data.json"

  etag = filemd5("./etl-configs/customer_segmentation_data.json")
}

resource "aws_s3_object" "jdbc-driver" {
  bucket = aws_s3_bucket.artifacts-bucket.id
  key    = "drivers/snowflake-jdbc-3.16.1.jar"
  source = "./drivers/snowflake-jdbc-3.16.1.jar"

  etag = filemd5("./drivers/snowflake-jdbc-3.16.1.jar")
}

resource "aws_s3_object" "spark-snowflake-driver" {
  bucket = aws_s3_bucket.artifacts-bucket.id
  key    = "drivers/spark-snowflake_2.13-2.16.0-spark_3.3.jar"
  source = "./drivers/spark-snowflake_2.13-2.16.0-spark_3.3.jar"

  etag = filemd5("./drivers/spark-snowflake_2.13-2.16.0-spark_3.3.jar")
}
