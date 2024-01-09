from datetime import timedelta
import logging
import os
import glob
import random
import shutil
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import ge_valid as ge
import pandas as pd
from datetime import datetime


@dag(
    dag_id="ingest_data",
    description="Validate data from a file by great_expectations",
    tags=["dsp", "validate", "alert"],
    schedule=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=1)
    # catchup=False
    # start_date=datetime(2024, 1, 1),
    # schedule_interval="* * * * *",
)
def ingestion():
    @task
    def read_file() -> pd.DataFrame:
        input_path = '/opt/data/folder_E'
        file_pattern = os.path.join(input_path, '*.csv')

        # Randomly select a file path
        file_paths = glob.glob(file_pattern)
        logging.info(file_paths)
        file_path = random.choice(file_paths)
        df = pd.read_csv(file_path)

        # Move the file to folder_B
        # destination_path = 'data/folder_B'
        # shutil.move(file_path, destination_path)
        
        # file_name = os.path.basename(file_path)

        return df
    
    # @task
    # def validate_file(df):
    #     # df, file_name = data
    #     df_ge = ge.from_pandas(df)
    #     expectation_suite = ge.dataset.util.create_expectation_suite()
    #     expectation_suite.add_expectation({
    #         "expectation_type": "expect_column_values_to_not_be_null",
    #         "kwargs": {
    #             "column": "reviewText"
    #         }
    #     })
    #     df_ge.validate(expectation_suite)
    #     return df, file_name
    
    # @task
    # def split_file(data):
    #     df, file_name = data
    #     df_null = df[df['reviewText'].isnull()]
    #     df_not_null = df[df['reviewText'].notnull()]
    #     return df_null, df_not_null, file_name

    @task
    def save_file(df: pd.DataFrame) -> None:
        # Get current time and date
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")

        # Include the timestamp in the filename
        file_path = f'/opt/data/folder_C/{timestamp}.csv'
        logging.info(f'Ingesting data to the file: {file_path}')
        
        df.to_csv(file_path, index=False)


    # Task relationships
    df = read_file()
    save_file(df)

    # @task
    # def get_validation() -> None:
    #     input = ("data/folder_A")
    #     output_success = ("data/folder_C")
    #     output_fail = ("data/folder_B")
    #     file_pattern = os.path.join(input, "*.csv")
    #     file_paths = glob.glob(file_pattern)

    #     for file_path in file_paths:
    #         ge.process_file(file_path, output_fail, output_success)

    # get_validation()

ingestion_dag = ingestion()
