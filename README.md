# Santex challenge

This project uses Terraform to create AWS resources and facilitates data loading onto Snowflake. It sets up the necessary infrastructure and scripts to automate the data pipeline.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Approach](#approach)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
- [Terraform](https://www.terraform.io/downloads.html) v0.12 or later
- AWS account with appropriate permissions
- Snowflake account and credentials
- [AWS CLI](https://aws.amazon.com/cli/) installed and configured

## Architecture
This project provisions the following AWS resources:
- S3 bucket: To store data files
- IAM roles and policies: To manage permissions
- AWS Glue: To orchestrate the ETL process
- Secrets Manager: To store Snowflake credentials
- CloudWatch: For logging and monitoring

The data is loaded into Snowflake using Snowflake's [SPARK CONNECTOR](https://docs.snowflake.com/en/user-guide/spark-connector-overview).

![image](https://github.com/user-attachments/assets/acfa01eb-52b1-4000-8dcf-565be16747a0)


## Approach


## Setup



1. **Create a Role for Terraform:**
   Create an IAM role in AWS with the following policies that allows Terraform to manage resources or:
   ```sh
   git clone https://github.com/yourusername/aws-snowflake-loader.git
   cd aws-snowflake-loader
   ```
   
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/aws-snowflake-loader.git
   cd aws-snowflake-loader
   ```

2. **Initialize Terraform:**
   ```sh
   terraform init
   ```

3. **Configure the secret :**
   Create a `terraform.tfvars` file and populate it with your configuration.
   ```hcl
   aws_region = "us-west-2"
   s3_bucket_name = "your-s3-bucket"
   snowflake_account = "your_snowflake_account"
   snowflake_user = "your_snowflake_user"
   snowflake_password = "your_snowflake_password"
   snowflake_database = "your_snowflake_database"
   snowflake_schema = "your_snowflake_schema"
   snowflake_warehouse = "your_snowflake_warehouse"
   ```

4. **Apply the Terraform configuration:**
   ```sh
   terraform apply
   ```

5. **Create a Secret in AWS Secrets Manager:**
   Store your Snowflake credentials in AWS Secrets Manager. The secret should contain the following keys: `sfUser`, `sfPassword`, `sfAccount`.
   ```sh
   aws secretsmanager create-secret --name snowflake-credentials --secret-string '{"sfUser":"your_snowflake_user","sfPassword":"your_snowflake_password","sfAccount":"your_snowflake_account"}'
   ```

6. **Create a Glue Connection to Snowflake:**
   Create an AWS Glue connection named "Snowflake connection" that holds the Snowflake account URL and references the secret created.
   ```sh
   aws glue create-connection --name "Snowflake connection" --connection-input '{"Name":"Snowflake connection","ConnectionType":"JDBC","ConnectionProperties":{"JDBC_CONNECTION_URL":"jdbc:snowflake://your_snowflake_account_url","SECRET_ID":"arn:aws:secretsmanager:your_region:your_account_id:secret:snowflake-credentials"}}'
   ```

## Usage

1. **Trigger the AWS Glue job:**
   The Glue job can be manually triggered, or you can set up an event source (e.g., S3 upload event) to automatically trigger it.

2. **Monitor the process:**
   Use CloudWatch to monitor the logs and ensure the data loading process completes successfully.

3. **Validate data in Snowflake:**
   Once the data is loaded, validate it in Snowflake using some queries. For example:
   ```sql
   -- Count the number of rows in a table
   SELECT COUNT(*) FROM your_table;

   -- Check for specific data
   SELECT * FROM your_table WHERE some_column = 'some_value';

   -- Get a summary of the data
   SELECT some_column, COUNT(*) FROM your_table GROUP BY some_column;
   ```

## Configuration
The following variables can be configured in `variables.tf` or `terraform.tfvars`:

- `aws_region`: AWS region where the resources will be created
- `s3_bucket_name`: Name of the S3 bucket
- `snowflake_account`: Snowflake account identifier
- `snowflake_user`: Snowflake user
- `snowflake_password`: Snowflake password
- `snowflake_database`: Snowflake database name
- `snowflake_schema`: Snowflake schema name
- `snowflake_warehouse`: Snowflake warehouse name

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify this README to better match your project's specifics, including any additional setup steps, usage details, or other relevant information.
