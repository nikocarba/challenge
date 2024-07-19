resource "aws_s3_bucket" "raw-bucket" {
    bucket = var.raw_bucket_name
    tags = var.s3_bucket_tags
}

resource "aws_s3_object" "raw-data" {
  bucket = aws_s3_bucket.raw-bucket.bucket
  key    = "customer_segmentation_data.csv"
  source = "data/customer_segmentation_data.csv"
}