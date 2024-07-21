variable "raw_bucket_name" {
  description = "The name of the S3 bucket that contains the raw data."
  type        = string
}

variable "artifacts_bucket_name" {
  description = "The name of the S3 bucket that contains artifacts for the project."
  type        = string
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

variable "glue_job_name" {
  description = "The name of the glue job."
  type        = string
}

variable "spark_arguments" {
  type = any
}
