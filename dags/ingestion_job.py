
from datetime import datetime, timedelta
import pandas as pd
import logging
import os
from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import get_current_context
from great_expectations.dataset import PandasDataset

FOLDER_A = 'Folder_A_test'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@task
def ingest_data(file_path):
    df = pd.read_csv(file_path)
    df = PandasDataset(df)

    # Validate using Great Expectations
    if df.expect_column_values_to_not_be_null('reviewText')['success']:
        output_path = 'Folder_C_ingested/ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'
    else:
        output_path = 'Folder_B_ingested/ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv'

    df.to_csv(output_path, index=False)
    logging.info(f'File ingested and saved to {output_path}')
    return output_path

with DAG(
    dag_id='ingestion_job',
    default_args=default_args,
    description='A DAG for ingesting CSV files',
    schedule_interval=timedelta(minutes=2),
    start_date=datetime.now() - timedelta(hours=1),
    tags=['example'],
) as dag:

    # Iterate over all CSV files in the specified folder
    for file in os.listdir(FOLDER_A):
        if file.endswith('.csv'):
            ingest_data_task = ingest_data(os.path.join(FOLDER_A, file))

ingest_data_dag = dag
