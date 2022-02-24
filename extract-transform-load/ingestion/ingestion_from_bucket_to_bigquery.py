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
dataset_name = "addresses"
dataset_id = f"{project_id}.{dataset_name}"
dataset = bigquery.Dataset(dataset_id)
file_name = "addresses"


try:
    dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
    logger.info(f"the dataset {dataset_name} was created successfully")
except google.api_core.exceptions.Conflict: 
    logger.info(f"the dataset {dataset_name} already exists")


table_id =   f"{project_id}.{dataset_name}.addresses"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("address_id", "INTEGER"),
        bigquery.SchemaField("addresse", "STRING"),
        bigquery.SchemaField("postal_code","INTEGER"),
        bigquery.SchemaField("phone_number","STRING"),
        bigquery.SchemaField("city_id","INTEGER"),
        bigquery.SchemaField("last_update","TIMESTAMP")],
    skip_leading_rows=0,
    source_format=bigquery.SourceFormat.CSV,
)

uri = f"gs://etl-pipeline-loading/{file_name}.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
logger.info("Loaded {} rows.".format(destination_table.num_rows))