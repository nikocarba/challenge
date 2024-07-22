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
}

variable "script_path" {
  description  = "The path in s3 to the glue job script"
  type         = string
}

variable "raw_table_name" {
  type = string
}