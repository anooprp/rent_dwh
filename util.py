import boto3
from boto3.s3.transfer import S3Transfer
import os
import psycopg2


def s3_file_download( bucket_name,file_key,output_filename):


    save_as =   output_filename
    transfer = S3Transfer(boto3.client('s3',
                                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID']
                                       , aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']))
    transfer.download_file(bucket_name, file_key, save_as)
    return save_as

def s3_delete_file(bucket,s3_filekey):
    transfer = S3Transfer(boto3.client('s3',
                                       aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID']
                                       , aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']))
    transfer.Object(bucket, s3_filekey).delete()

def get_postgres_con():


    conn = psycopg2.connect(host=os.environ['ODS_HOST'], port=os.environ['ODS_PORT'],
                            user=os.environ['ODS_USERNAME'], password=os.environ['ODS_PASSWORD'],
                            dbname=os.environ['ODS_DBNAME'])
    return conn
