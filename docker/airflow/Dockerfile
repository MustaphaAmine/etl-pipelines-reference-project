FROM apache/airflow:2.2.4

ARG AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW_HOME=${AIRFLOW_HOME}

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the owner of the files in AIRFLOW_HOME to the user airflow
RUN chown -R airflow: ${AIRFLOW_HOME}
# Copy the entrypoint.sh from host to container (at path AIRFLOW_HOME)
COPY ./start-airflow.sh ./start-airflow.sh
# Set the entrypoint.sh file to be executable
RUN chmod +x ./start-airflow.sh
# Set the username to use
USER airflow
# Create the folder dags inside $AIRFLOW_HOME
RUN mkdir -p ${AIRFLOW_HOME}/dags
# Expose ports (just to indicate that this container needs to map port)
EXPOSE 8080
# Execute start-airflow.sh
CMD ["bash","./start-airflow.sh" ]