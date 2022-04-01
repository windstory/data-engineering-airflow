FROM apache/airflow:2.2.4-python3.9

#ARG DEST_INSTALL=/home/airflow

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get autoremove -yqq --purge \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /
RUN pip install -U pip setuptools wheel \
	&& pip install --requirement /requirements.txt

COPY airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

USER root

COPY entrypoint.sh /

RUN chown -R "airflow" "${AIRFLOW_HOME}"

USER airflow
WORKDIR ${AIRFLOW_HOME}
ENTRYPOINT ["/entrypoint.sh"]