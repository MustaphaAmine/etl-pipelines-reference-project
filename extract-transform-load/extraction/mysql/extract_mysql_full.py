import pymysql
import csv
import json
import configparser
from google.cloud import storage

import logging
from logging.config import fileConfig

# initiate the logger
fileConfig('./logging_conf.ini')
logger = logging.getLogger()

def establish_connection_with_mysql_db():
    """Getting the connection credentials from the pipeline.conf file
    And creating a connection instance with a MySql DataBase"""

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
        return None
    else:
        logger.info("MySQL connection established!")
        return conn

def extract_data(local_filename):
    """This function create a simple Query """
    conn = establish_connection_with_mysql_db()
    m_query = """
    WITH address_all_info AS (
            SELECT
                address_id,
                address,
                city_name,
                country_name
            FROM 
                address
            LEFT JOIN 
                city USING(city_id)
            LEFT JOIN 
                country USING(country_id)),
                customer_add_address_info AS (
            SELECT 
                customer_id,
                last_name AS cust_last_name, 
                first_name AS cust_first_name,
                email AS cust_email,
                active AS cust_active,
                create_date,
                country_name AS cust_country,
                city_name AS cust_city,
                address AS cust_address
            FROM customer
            LEFT JOIN address_all_info USING(address_id)),
                staff_add_address_info AS (
            SELECT 
                staff_id,
                last_name AS staff_last_name,
                first_name AS staff_first_name,
                email AS staff_email,
                active AS staff_active,
                country_name AS staff_country,
                city_name AS staff_city,
                address AS staff_address
            FROM staff
            LEFT JOIN address_all_info USING(address_id))
        SELECT 
            rental_id,
            rental_date,
            return_date,
            rating,
            -- staff
            staff_id,
            staff_last_name,
            staff_first_name,
            staff_email,
            staff_active,
            staff_country,
            staff_city,
            staff_address,
            -- customer
            customer_id,
            cust_last_name,
            cust_first_name,
            cust_email,
            cust_active,
            create_date,
            cust_country,
            cust_city,
            cust_address
        FROM 
            rental
        LEFt JOIN staff_add_address_info USING(staff_id)
        LEFT JOIN customer_add_address_info USING(customer_id)
    """

    m_cursor = conn.cursor()
    m_cursor.execute(m_query)
    results = m_cursor.fetchall()

    with open(local_filename, 'w') as fp:
        for result in results:
            f_result = dict()
            f_result["rental_id"] = result[0]
            f_result["rental_date"] = result[1].strftime("%Y-%m-%d")
            f_result["return_date"] = result[2].strftime("%Y-%m-%d")
            f_result["rating"] = result[3]
            f_result["staff"] = dict()
            f_result["staff"]["id"] = result[4]
            f_result["staff"]["last_name"] = result[5]
            f_result["staff"]["first_name"] = result[6]
            f_result["staff"]["email"] = result[7]
            f_result["staff"]["active"] = result[8]
            f_result["staff"]["address"] = dict()
            f_result["staff"]["address"]["country"] = result[9]
            f_result["staff"]["address"]["city"] = result[10]
            f_result["staff"]["address"]["address"] = result[11]
            f_result["customer"] = dict()
            f_result["customer"]["id"] = result[12]
            f_result["customer"]["last_name"] = result[13]
            f_result["customer"]["first_name"] = result[14]
            f_result["customer"]["email"] = result[15]
            f_result["customer"]["active"] = result[16]
            f_result["customer"]["create_date"] = result[17].strftime("%Y-%m-%d")
            f_result["customer"]["address"] = dict()
            f_result["customer"]["address"]["country"] = result[18]
            f_result["customer"]["address"]["city"] = result[19]
            f_result["customer"]["address"]["address"] = result[20]
            fp.write(json.dumps(f_result)+'\n')

        logger.info(f"{local_filename} was successfully created and stored")

    fp.close()
    m_cursor.close()
    conn.close()

def uploading_data_to_gcs_bucket():
    """ 
    Upload data to a bucket
    Explicitly use service account credentials by specifying the private key file
    the folder keys that contains the service account credentials is not uploaded to Github for security measures
    """
    storage_client = storage.Client.from_service_account_json(
        './keys/etl-pipelines-key.json')
    
    local_filename = "rentals.json"
    bucket_name = "etl-pipeline-loading"
    blob_name = local_filename

    extract_data(local_filename)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_filename)
    logger.info(f"{local_filename} was successfully uploaded to the bucket")

uploading_data_to_gcs_bucket()

