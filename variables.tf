variable "project" {
  description = "The name of the project."
  type        = string
}

variable "owner" {
  description = "The name of the owner of the project."
  type        = string
}

variable "spark_arguments" {
  description = "Default arguments for the glue job."
  type = any
}

variable "raw_table_name" {
  description = "Raw table name to process."
  type = string
}

variable "snowflake_secret_name" {
  description = "Previously created secret name."
  type = string
}