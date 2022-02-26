# Move to the AIRFLOW HOME directory
cd $AIRFLOW_HOME
#
# Initiliase the metadatabase
airflow db init
# Create User
airflow users create -e "admin@airflow.com"\
                     -r "Admin" \
                     -u "airflow" \
                     -p "airflow" \
                     -f "airflow" \
                     -l "airflow"              
# Run the scheduler in background
airflow scheduler &> /dev/null &
# Run the web sever in foreground (for docker logs)
airflow webserver