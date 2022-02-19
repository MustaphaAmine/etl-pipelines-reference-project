from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client.from_service_account_json(
    './keys/etl-pipelines-key.json')
table_id =   "etl-pipelines.addresses.country"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("country_id", "STRING"),
        bigquery.SchemaField("country_name", "STRING"),
        bigquery.SchemaField("update_date","TIMESTAMP")
    ],
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
)

uri = "gs://etl-pipeline-loading/country.csv"

load_job = client.load_table_from_uri(
    uri, table_id, job_config=job_config
)  # Make an API request.

load_job.result()  # Waits for the job to complete.

destination_table = client.get_table(table_id)  # Make an API request.
print("Loaded {} rows.".format(destination_table.num_rows))