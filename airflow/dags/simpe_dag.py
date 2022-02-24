# from imaplib import Time2Internaldate
from airflow import DAG
from datetime import timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago

dag = DAG(
    'simple_dag',
    description = 'a simple dag',
    schedule_interval = timedelta(days=1),
    start_date = days_ago(1),
)

t1 = BashOperator(
    task_id='print_date',
    bash_command = 'date',
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