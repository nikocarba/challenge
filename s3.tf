resource "aws_s3_bucket" "raw-bucket" {
    bucket = var.raw_bucket_name
    tags = var.s3_bucket_tags
}

resource "aws_s3_bucket" "artifacts-bucket" {
    bucket = var.artifacts_bucket_name
    tags = var.s3_bucket_tags
}

resource "aws_s3_object" "raw-data" {
  bucket = aws_s3_bucket.raw-bucket.bucket
  key    = "${local.raw_table_name}.csv"
  source = "data/${local.raw_table_name}.csv"

  etag = filemd5("data/${local.raw_table_name}.csv")
}

resource "aws_s3_object" "glue-script" {
  bucket = aws_s3_bucket.artifacts-bucket.bucket
  key    = "scripts/etl.py"
  source = "scripts/etl.py"

  etag = filemd5("scripts/etl.py")
}