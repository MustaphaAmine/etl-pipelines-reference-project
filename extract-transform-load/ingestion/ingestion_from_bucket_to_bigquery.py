from google.cloud import bigquery
import google
import logging
from logging.config import fileConfig

# initiate the logger
fileConfig('./logging_conf.ini')
logger = logging.getLogger()

# Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(
    './keys/etl-pipelines-key.json')
project_id = "etl-pipelines"
dataset_name = "library_management"
dataset_id = f"{project_id}.{dataset_name}"
dataset = bigquery.Dataset(dataset_id)
file_name = "rentals"

try:
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    logger.info(f"the dataset {dataset_name} was created successfully")
except google.api_core.exceptions.Conflict: 
    logger.info(f"the dataset {dataset_name} already exists")

table_id =   f"{project_id}.{dataset_name}.rentals_production"

job_config = bigquery.LoadJobConfig(
    schema=[
        	bigquery.SchemaField("rental_id","INTEGER"),
            bigquery.SchemaField("rental_date","DATE", mode="NULLABLE"),
            bigquery.SchemaField("return_date","DATE", mode="NULLABLE"),
            bigquery.SchemaField("rating","INTEGER", mode="NULLABLE"),
            bigquery.SchemaField(
                "staff",
                "RECORD",
                mode="REPEATED",
                fields = [
                        bigquery.SchemaField("id","INTEGER"),
                        bigquery.SchemaField("last_name","STRING", mode="NULLABLE"),
                        bigquery.SchemaField("first_name","STRING",mode="NULLABLE"),
                        bigquery.SchemaField("email","STRING", mode="NULLABLE"),
                        bigquery.SchemaField("active","BOOLEAN", mode="NULLABLE"),
                        bigquery.SchemaField(
                            "address",
                            "RECORD",
                            mode="REPEATED",
                            fields = [
                                    bigquery.SchemaField("country","STRING", mode="NULLABLE"),
                                    bigquery.SchemaField("city","STRING", mode="NULLABLE"),
                                    bigquery.SchemaField("address","STRING", mode="NULLABLE"),
                                    ])]),
            bigquery.SchemaField(
                "customer",
                "RECORD",
                mode="REPEATED",
                fields = [
                        bigquery.SchemaField("id","INTEGER"),
                        bigquery.SchemaField("last_name","STRING", mode="NULLABLE"),
                        bigquery.SchemaField("first_name","STRING", mode="NULLABLE"),
                        bigquery.SchemaField("email","STRING", mode="NULLABLE"),
                        bigquery.SchemaField("active","BOOLEAN", mode="NULLABLE"),
                        bigquery.SchemaField("create_date","DATE", mode="NULLABLE"),
                        bigquery.SchemaField(
                            "address",
                            "RECORD",
                            mode="REPEATED",
                            fields = [ 
                                    bigquery.SchemaField("country","STRING", mode="NULLABLE"),
                                    bigquery.SchemaField("city","STRING", mode="NULLABLE"),
                                    bigquery.SchemaField("address","STRING", mode="NULLABLE"),
                                    ])]),
            ],
    source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
)

uri = f"gs://etl-pipeline-loading/{file_name}.json"
load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.
load_job.result()  # Waits for the job to complete.
destination_table = client.get_table(table_id)  # Make an API request.
logger.info("Loaded {} rows.".format(destination_table.num_rows))