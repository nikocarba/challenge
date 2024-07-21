import boto3
from botocore.exceptions import ClientError
import os
import sys
import json
from datetime import datetime as dt
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, to_date, when, col, lower, regexp_replace
from py4j.java_gateway import java_import
import logging

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(getattr(logging, os.getenv('LOG_LEVEL', 'INFO')))
logger.info('Start execution')

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

def get_json_parameters(etl_name, s3_artifacts_bucket):
    """
    Gets the job configurations for the ETL from a json file in s3
    """
    file_path = f'etl_configs/{etl_name}.json'

    s3_object = s3.get_object(Bucket=s3_artifacts_bucket, Key=file_path)
    json_data = s3_object['Body'].read().decode('utf-8')
    job_params = json.loads(json_data)
    return job_params
    
def read_csv(bucket_name, filename):
    """
    Reads S3 data stored as .csv file
    """
    path = f's3://{bucket_name}/{filename}'
    
    df = spark.read\
        .format("csv")\
        .option("header", "true")\
        .load(path)
    return df
    
def get_secret(secret_name):    
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    secret_params = json.loads(secret)
    return secret_params

def rename_col(df, mapping):
    for col in mapping:
        df = df.withColumnRenamed(col, mapping[col])
    return df
    
def standardize_col_name(df):
    for col in df.schema.names:
        df = df.withColumnRenamed(col, col.upper().replace(" ", "_"))
    return df

def normalize_dates(df, col_names):
    for col in col_names:
        df = df.withColumn(col, regexp_replace(col, "/", "-"))
        df = df.withColumn(col, to_date(df[col],"dd-MM-yyyy"))
    return df

def normalize_genders(df, gender_cols):
    for col in gender_cols:
        df.withColumn(col, when(lower(df[col]) == "female","F")
          .when(lower(df[col]) == "male","M")
          .otherwise("Unknown"))
    return df

snowflake_db = 'SNOWFLAKE_DATABASE'
snowflake_schema = 'SNOWFLAKE_SCHEMA'
secret_name = 'snowflake_ncarballal'
snowflake_table = 'CUSTOMER_SEGMENTATION_DATA'

secret = get_secret(secret_name)


# csvDf.show()

# java_import(spark._jvm, SNOWFLAKE_SOURCE_NAME)
# spark._jvm.net.snowflake.spark.snowflake.SnowflakeConnectorUtils.enablePushdownSession(spark._jvm.org.apache.spark.sql.SparkSession.builder().getOrCreate())

sfOptions = {
    "sfURL" : secret['sfAccount'] + ".snowflakecomputing.com",
    "sfUser" : secret['sfUser'],
    "sfPassword" : secret['sfPassword'],
    "sfDatabase" : snowflake_db,
    "sfSchema" : snowflake_schema,
    "sfWarehouse" : 'COMPUTE_WH',
    "sfRole": 'ACCOUNTADMIN'
}

# l = [(1, "i"), (2, "h"), (3, "g"), (4, "f"), (5, "e"), (6, "d"), (7, "c"), (8, "b"), (9, "a")]
# df2 = spark.createDataFrame(l, ['ID', 'DESC'])

mapping = {
    "Behavioral Data": "BEHAVIORAL_DATA_POLICY",
    "Insurance Products Owned": "INSURANCE_PRODUCTS_OWNED_POLICY"
}

df = read_csv("raw-bucket-test-terraform-ncarballal", "customer_segmentation_data.csv")
df = rename_col(df, mapping)

df = standardize_col_name(df)
df = normalize_dates(df, ['PURCHASE_HISTORY'])
df = normalize_genders(df, ["GENDER"])
df = df.withColumn('SEGMENTATION_GROUP', regexp_replace('SEGMENTATION_GROUP', "Segment", ""))
df = df.withColumn('BEHAVIORAL_DATA_POLICY', regexp_replace('BEHAVIORAL_DATA_POLICY', "policy", ""))
df = df.withColumn('INSURANCE_PRODUCTS_OWNED_POLICY', regexp_replace('INSURANCE_PRODUCTS_OWNED_POLICY', "policy", ""))
df = df.withColumn('PREFERRED_COMMUNICATION_CHANNEL', regexp_replace('SEGMENTATION_GROUP', " Meeting", ""))

# CUSTOM TRANSFORMATIONS

df.write.format(SNOWFLAKE_SOURCE_NAME)\
    .options(**sfOptions)\
    .option("dbtable", snowflake_table)\
    .mode("overwrite").save()


job.commit()
