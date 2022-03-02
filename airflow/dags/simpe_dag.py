# from imaplib import Time2Internaldate
from airflow import DAG
from datetime import timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from functions.helpers import test_function
from executable.extract_mysql_full import uploading_data_to_gcs_bucket
from airflow.utils.dates import days_ago

dag = DAG(
    'simple_dag',
    description = 'a simple dag',
    schedule_interval = timedelta(days=1),
    start_date = days_ago(1),
)

t1 = PythonOperator(
    task_id='upload_data_to_bigquery',
    python_callable = uploading_data_to_gcs_bucket,
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past = False,
    bash_command='sleep 3',
    dag=dag,
)

t3 = BashOperator(
    task_id='print_end', 
    depends_on_past=False, 
    bash_command='echo \'end\'', 
    dag=dag, )

t1>>t2
t2>>t3