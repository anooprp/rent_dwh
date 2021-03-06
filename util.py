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


def s3_move_file(bucket,s3_filekey):
    resource = boto3.resource('s3', 'us-east-1',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                              aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])


    copy_source = {
        'Bucket': bucket,
        'Key': s3_filekey
    }
    other_key='Processed/'+s3_filekey
    resource.meta.client.copy(copy_source,bucket, other_key)
    resource.Object(bucket, s3_filekey).delete()

def get_postgres_con():


    conn = psycopg2.connect(host=os.environ['ODS_HOST'], port=os.environ['ODS_PORT'],
                            user=os.environ['ODS_USERNAME'], password=os.environ['ODS_PASSWORD'],
                            dbname=os.environ['ODS_DBNAME'])
    return conn


def get_columns_postgres(v_table_name):
    con = get_postgres_con()
    cur = con.cursor()
    cur.execute(
        "select * from {tab_name} where 1=2".format(tab_name=v_table_name))
    columns = list(map(lambda x: x[0], cur.description))
    con.close()

    return ','.join(columns)
