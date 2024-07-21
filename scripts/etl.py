import boto3
from botocore.exceptions import ClientError
import os
import sys
import json
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext
from pyspark.sql.functions import to_date, regexp_replace, expr, lpad
import logging

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'TABLE_NAME', 'RAW_BUCKET'])
table_name = args['TABLE_NAME']
raw_bucket = args['RAW_BUCKET']

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
        df = df.withColumn(col, lpad(df[col], 10, '0'))
        df = df.withColumn(col, to_date(df[col],"MM-dd-yyyy"))
    return df

def normalize_genders(df, gender_cols):
    for col in gender_cols:
        df = df.withColumn(col, expr("CASE WHEN lower(GENDER) = 'male' THEN 'M' " + 
           "WHEN lower(GENDER) = 'female' THEN 'F' WHEN GENDER IS NULL THEN ''" +
          "ELSE GENDER END"))
    return df

def remove_from_col(col_name, str_to_remove):
    return df.withColumn(col_name, regexp_replace(col_name, str_to_remove, ""))


snowflake_db = 'SNOWFLAKE_DATABASE'
snowflake_schema = 'SNOWFLAKE_SCHEMA'
secret_name = 'snowflake_ncarballal'
snowflake_table = 'CUSTOMER_SEGMENTATION_DATA'

secret = get_secret(secret_name)

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

mapping = {
    "Behavioral Data": "BEHAVIORAL_DATA_POLICY",
    "Insurance Products Owned": "INSURANCE_PRODUCTS_OWNED_POLICY"
}

df = read_csv(raw_bucket, f"{table_name}.csv")
df = rename_col(df, mapping)

df = standardize_col_name(df)
df = normalize_dates(df, ['PURCHASE_HISTORY'])
df = normalize_genders(df, ["GENDER"])

# CUSTOM TRANSFORMATIONS FOR CUSTOMER_SEGMENTATION_DATA
df = remove_from_col('PREFERRED_COMMUNICATION_CHANNEL', " Meeting")
df = remove_from_col('CUSTOMER_PREFERENCES', " Meeting")
df = remove_from_col('INSURANCE_PRODUCTS_OWNED_POLICY', "policy")
df = remove_from_col('BEHAVIORAL_DATA_POLICY', "policy")
df = remove_from_col('SEGMENTATION_GROUP', "Segment")

df.write.format(SNOWFLAKE_SOURCE_NAME)\
    .options(**sfOptions)\
    .option("dbtable", snowflake_table)\
    .mode("overwrite").save()

job.commit()
