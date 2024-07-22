variable "project" {
  description = "The name of the project."
  type        = string
}

variable "owner" {
  description = "The name of the owner of the project."
  type        = string
}

variable "spark_arguments" {
  type = any
}

variable "raw_table_name" {
    type = string
}

variable "snowflake_secret_name" {
    type = string
}