<!-- # Extract
# Data Extraction
## MySQL
## mysql binlog replication 
In the example, I read from the default binlog file, in case the MySQL administrator uses a customed file naming scheme, you can specify the new path as a value to to the `log_file` parameter when creating the BinLogStreamReader. See [the documentation for the BinLogStreamReader](https://python-mysql-replication.readthedocs.io/en/latest/binlogstream.html) for more.

## MongoDB


## REST-API


Transformation
    Drop duplicate (using distinct Or window function) page 117
    URL parsing page 119


Generate mock data [here](http://filldb.info/)
Generate mock data [here](https://www.mockaroo.com/)

# Data Ingestion / Loading

# Data Transformation 


# Orchestrating a pipeline :
Follow the installation instruction from the the official [Airflow Quick Start Guide](https://airflow.apache.org/docs/apache-airflow/stable/start/index.html)

export AIRFLOW_HOME=~/airflow
AIRFLOW_VERSION=2.2.3
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

airflow users create \
    --username mustaphamine \
    --firstname mustapha \
    --lastname debbih \
    --role Admin \
    --email fm_debbih@esi.dz

Airflow additional Pipeline tasks :
    Alerts & Notifications:
    Data Validation chekcs

Advanced Orchestration Configurations
    Coupled Vs UnCoupled pipeline tasks
    Spliting Up DAGs
    Coordinating Multiple DAGs with Sensors

    Managed Airflow Options:
        Similar to some of the build versus buy decisions, hosting Airflow on your own versus choosing a managed solution depends on your particular situation:
            Do you have a systems operations team that can help you self host?
            Do you have the budget to spend on a managed service?
            How many DAGs and tasks make up your pipelines?
            Are you running at a high enough scale to require more complex Airflow executors?
            What are your security and privacy requirements? 
            Are you comfortable allowing an external service to connect to your  internal data and systems?
Other Orchestration frameworks:
    [Kubeflow pipelines](https://www.kubeflow.org/) is geared toward machine learning pipeline orchestration,it is also well supported and popular in the ML community.
    Orchetration of the transform step for data models [dbt by Fishtown Analytics](https://www.getdbt.com/) is an excellent option.

# Data Validation in Pipelines : 
    Validate Early, Validate Often:
        Source System Data Quality
        Data Ingestion Risks
 -->