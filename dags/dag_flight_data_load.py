from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

from datetime import datetime
from datetime import timedelta

from config import flight_data_load_config as config

import os
import csv

def get_Redshift_connection():
    hook = PostgresHook(postgres_conn_id='redshift_dev_db')    
    return hook.get_conn().cursor()

def extract(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    return csv.reader(f)

def transform(data):
    header = data[0]
    print(header)
    return data[1:]
        
def load(schema, table, rows):
    values = []
    for row in rows:
        (dest_country_name, origin_country_name, cnt) = row
        values.append("('{}','{}',{})".format(dest_country_name, origin_country_name, cnt))

    cur = get_Redshift_connection()
    insert_sql = """DELETE FROM {schema}.{table};INSERT INTO {schema}.{table} VALUES """\
        .format(schema=schema,table=table)\
         + ",".join(values)
    try:
        cur.execute(insert_sql)
        cur.execute("Commit;")
    except Exception as e:
        cur.execute("Rollback;")
        raise

def etl(**context):
    file_path = context["params"]["file_path"]
    schema = context["params"]["schema"]
    table = context["params"]["table"]
    data = extract(file_path)
    rows = transform(list(data))
    load(schema, table, rows)

dag_flight_data = DAG(
    dag_id = 'dag_flight_data',
    start_date = datetime(2022,3,20),
    schedule_interval = '@once', 
    catchup = False,
    max_active_runs = 1,
    default_args = {
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
    }
)

etl_task = PythonOperator(
    task_id = 'perform_etl',
    python_callable = etl,
    params = {
        'file_path': config['data_file_path'],
        'schema': config['schema'],
        'table': config['table']
    },
    provide_context=True,
    dag = dag_flight_data)