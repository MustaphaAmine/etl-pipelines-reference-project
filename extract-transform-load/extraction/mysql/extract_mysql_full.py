import pymysql
import csv
import configparser
from google.cloud import storage

import logging
from logging.config import fileConfig

# initiate the logger
fileConfig('./logging_conf.ini')
logger = logging.getLogger()

# Getting the connection credentials from the pipeline.conf file
parser = configparser.ConfigParser()
parser.read("pipeline.conf")
hostname = parser.get("mysql_config","hostname")
port = parser.get("mysql_config","port")
username = parser.get("mysql_config","username")
dbname = parser.get("mysql_config","database")
password = parser.get("mysql_config","password")

conn = pymysql.connect(host=hostname,
            user=username,
            db=dbname,
            port=int(port),
            password=password)

# it would be best if we here use the logging module instead of the print function
if conn is None:
    logger.error("Error connecting to MySQL database")
else:
    logger.info("MySQL connection established!")

m_query = "SELECT * FROM address;"
local_filename = "addresses.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()
# print(type(results))
# t = [s for s in (1,2,3)
# print(t)

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp)
    csv_w.writerows(results)
    logger.info(f"{local_filename} was successfully created and stored")

fp.close()
m_cursor.close()
conn.close()

""" Upload data to a bucket"""
# Explicitly use service account credentials by specifying the private key file
# the folder keys that contains the service account credentials is not uploaded to Github for security measures
storage_client = storage.Client.from_service_account_json(
    './keys/etl-pipelines-key.json')

bucket_name = 'etl-pipeline-loading'
blob_name = 'addresses.csv'

bucket = storage_client.get_bucket(bucket_name)
blob = bucket.blob(blob_name)
blob.upload_from_filename(local_filename)
logger.info(f"{local_filename} was successfully uploaded to the bucket")