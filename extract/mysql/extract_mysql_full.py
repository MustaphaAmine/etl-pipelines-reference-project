import pymysql
import boto3
import csv
import configparser
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

# it would be best if we here use the logging module instead
if conn is None:
    logger.error("Error connecting to MySQL database")
else:
    logger.info("MySQL connection established!")

m_query = "SELECT * FROM posts;"
local_filename = "posts_extract.csv"

m_cursor = conn.cursor()
m_cursor.execute(m_query)
results = m_cursor.fetchall()

with open(local_filename, 'w') as fp:
    csv_w = csv.writer(fp)
    csv_w.writerows(results)

fp.close()
m_cursor.close()
conn.close()