from datetime import datetime, timedelta
import pandas as pd
import logging
import os
from airflow import DAG
from airflow.decorators import task
from great_expectations.dataset import PandasDataset

FOLDER_A = 'Folder_A_test'
FOLDER_B = 'Folder_B_ingested_test'
FOLDER_C = 'Folder_C_ingested_test'

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'airflow'
}

@task
def ingest_data(file_path):
    logger.info(f'Starting to read {file_path}')
    df = pd.read_csv(file_path)

    ge_df = PandasDataset(df)
    if not ge_df.expect_column_to_exist('reviewText')['success']:
        logger.info('reviewText column does not exist in the DataFrame')
        return

    non_null_df = df[df['reviewText'].notna()]
    null_df = df[df['reviewText'].isna()]

    if len(non_null_df) == len(df):
        # all values in "reviewText" are non-null -> Folder_B
        output_path = os.path.join(FOLDER_C, 'ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv')
        non_null_df.to_csv(output_path, index=False)
        logger.info(f'Success: All non-null rows ingested and saved to {output_path}')
    elif len(null_df) == len(df):
        # all values in "reviewText" are null -> Folder_C
        output_path = os.path.join(FOLDER_B, 'ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '.csv')
        null_df.to_csv(output_path, index=False)
        logger.info(f'Success: All null rows ingested and saved to {output_path}')
    else:
        # if values are mixed non-null and null
        output_path_non_null = os.path.join(FOLDER_C, 'ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_non_null.csv')
        output_path_null = os.path.join(FOLDER_B, 'ingested_' + datetime.now().strftime('%Y%m%d%H%M%S') + '_null.csv')
        non_null_df.to_csv(output_path_non_null, index=False)
        null_df.to_csv(output_path_null, index=False)
        logger.info(f'Success: Split mixed rows and saved to {output_path_non_null} and {output_path_null}')

    try:
        os.remove(file_path)
        logger.info(f'Successfully removed {file_path}')
    except Exception as e:
        logger.error(f'Error while removing {file_path}: {str(e)}')

with DAG(
    dag_id='ingestion_job',
    default_args=default_args,
    description='A DAG for ingesting CSV files',
    schedule_interval=timedelta(minutes=1),
    start_date=datetime.now() - timedelta(hours=1)
) as dag:

    for file in os.listdir(FOLDER_A):
        if file.endswith('.csv'):
            file_path = os.path.join(FOLDER_A, file)
            ingest_data_task = ingest_data(file_path)

ingest_data_dag = dag