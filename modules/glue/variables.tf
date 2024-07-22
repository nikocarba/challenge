variable "glue_job_name" {
  description = "The name of the glue job."
  type        = string
}

variable "spark_arguments" {
  description = "Default arguments for the glue job."
  type = any
}

variable "spark_configurations" {
  description = "Configurations for the glue job."
  type = any
}

variable "artifacts_bucket_name" {
  description = "The name of the artifacts bucket where the script is stored."
  type = string
}

variable "script_path" {
  description = "Path to the script in s3."
  type = string
}

variable "glue_role" {
  description = "Name of the glue role."
  type = string
}

variable "glue_tags" {
  description = "Tags for the glue job."
  type = any
}