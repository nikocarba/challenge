variable "raw_bucket_name" {
  description = "The name of the S3 bucket that contains the raw data."
  type        = string
  default     = "raw-bucket-test-terraform-ncarballal"
}

variable "s3_bucket_tags" {
  description = "Tags for the S3 bucket"
  type        = map(string)
  default = {
    Name        = "Raw data bucket"
    Environment = "Dev"
    Project     = "Test terraform and snowflake"
    Owner       = "Nicolas Carballal"
  }
}