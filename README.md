# Santex challenge

This project uses Terraform to create AWS resources and facilitates data loading onto Snowflake. It sets up the necessary infrastructure and scripts to automate the data pipeline.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Architecture](#architecture)
- [Approach](#approach)
- [Setup](#setup)
- [Usage](#usage)
- [Configuration](#configuration)

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


## Setup

1. **Create a Role for Terraform:**
   Create an IAM role in AWS with a basic policy that allows Terraform to manage resources. Here’s an example of a policy that provides the necessary permissions:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "ec2:*",
           "s3:*",
           "iam:*",
           "rds:*",
           "lambda:*",
           "cloudwatch:*",
           "secretsmanager:*",
           "glue:*"
         ],
         "Resource": "*"
       }
     ]
   }
   ```
   Attach this policy to the new IAM role.

2. **Configure AWS Credentials:**
   Use the AWS CLI to configure credentials for Terraform to use. The account used for this configuration will be used for the following steps, so it should have permissions to deploy the entire architecture, create a secret in Secrets Manager, and create a Glue connection.
   ```sh
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, default region name, and output format when prompted.

3. **Create a Secret in AWS Secrets Manager:**
   Store your Snowflake credentials in AWS Secrets Manager. The secret should contain the following keys: `sfUser`, `sfPassword`, `sfAccount`.
   ```sh
   aws secretsmanager create-secret --name snowflake-credentials --secret-string '{"sfUser":"your_snowflake_user","sfPassword":"your_snowflake_password","sfAccount":"your_snowflake_account"}'
   ```

4. **Create a Glue Connection to Snowflake:**
   Create an AWS Glue connection named "Snowflake connection" that holds the Snowflake account URL and references the secret just created in the AWS console. The glue job in the project used to load data onto Snowflake      will need this connection.

5. **Clone the repository:**
   ```sh
   git clone https://github.com/nikocarba/challenge.git
   cd challenge
   ```

6. **Initialize Terraform:**
   ```sh
   terraform init
   ```

7. **Configure Terraform variable:**
   Assign the secret name you created on step 3 to the variable "snowflake_secret_name" in terraform.tfvars file

8. **Plan and apply the Terraform configuration:**
   ```sh
   terraform plan
   terraform apply
   ```

## Usage

1. **Trigger the AWS Glue job:**
   The Glue job can be manually triggered, or you can set up an event source (e.g., S3 upload event) to automatically trigger it.
   ```sh
   aws glue start-job-run --job-name "load-to-snowflake-dataengineer-challenge-ncarballal"
   ```
   
3. **Monitor the process:**
   Use CloudWatch to monitor the logs and ensure the data loading process completes successfully.

4. **Validate data in Snowflake:**
   Once the data is loaded, validate it in Snowflake using some queries. For example:
   ```sql
   -- Count the number of rows in a table
   SELECT COUNT(*) FROM CUSTOMER_SEGMENTATION_DATA;

   -- Check there are only two genders
   SELECT GENDER, COUNT(*) FROM CUSTOMER_SEGMENTATION_DATA 
   GROUP BY GENDER

   -- Check for null values
   SELECT COUNT(*) FROM CUSTOMER_SEGMENTATION_DATA
   WHERE PURCHASE_HISTORY IS NULL

   -- Check min and max dates
   SELECT MIN(PURCHASE_HISTORY), MAX(PURCHASE_HISTORY) FROM CUSTOMER_SEGMENTATION_DATA
   ```
