output "jdbc-driver" {
    value = aws_s3_object.jdbc-driver.key
}

output "spark-snowflake-driver" {
    value = aws_s3_object.spark-snowflake-driver.key
}