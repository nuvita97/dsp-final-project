from datetime import timedelta, datetime
import logging
import os
import glob
import random
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import pandas as pd
import great_expectations as ge
import psycopg2
from utils import alert_user_by_email, write_logs_to_db


@dag(
    dag_id="ingest_data",
    description="Validate data and split into 2 folders",
    tags=["dsp", "ingest", "validate", "alert"],
    schedule=timedelta(minutes=1),
    start_date=days_ago(n=0, hour=1),
    catchup=False
    # start_date=datetime(2024, 1, 1),
    # schedule_interval="* * * * *",
)
def ingestion():

    @task
    def read_file() -> pd.DataFrame:
        input_path = '/opt/data/folder_A/'
        file_pattern = os.path.join(input_path, '*.csv')
        # Randomly select a file path
        file_paths = glob.glob(file_pattern)
        file_path = random.choice(file_paths)
        logging.info(file_path)
        df = pd.read_csv(file_path)
        df['file_name'] = os.path.basename(file_path)
        # Remove file
        os.remove(file_path)
        return df
    

    @task
    def validate_data(df) -> pd.DataFrame:
        context = ge.DataContext('gx')
        suite = context.get_expectation_suite(expectation_suite_name='csv_expectations')
        df['validated'] = ''
        for index, row in df.iterrows():
            row_df = pd.DataFrame([row])
            batch = ge.dataset.PandasDataset(row_df, expectation_suite=suite)
            logging.info(batch.validate())
            # If the row is not valid, set the Problem value in meta.desc
            if not batch.validate().success:
                for valid_case in batch.validate().results:
                    if not valid_case.success:
                        df.at[index, 'validated'] = valid_case['expectation_config']['meta']['desc']
                        break
        logging.info(df[['file_name', 'validated']])
        return df


    @task
    def split_file(df):
        # Split the DataFrame into two new DataFrames
        df_invalid = df[df['validated'].str.len() > 0]
        df_valid = df[df['validated'].str.len() == 0]
        # Get current time and date
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the DataFrame with null values to a CSV file in folder_B
        file_path_invalid = f'/opt/data/folder_B/invalid_{timestamp}.csv'
        logging.info(f'Saving invalid data to the file: {file_path_invalid}')
        df_invalid.to_csv(file_path_invalid, index=False)
        # Save the DataFrame without null values to a CSV file in folder_C
        file_path_valid = f'/opt/data/folder_C/valid_{timestamp}.csv'
        logging.info(f'Saving valid data to the file: {file_path_valid}')
        df_valid.to_csv(file_path_valid, index=False)
        return df_invalid



    @task
    def alert_errors(df_invalid):
        if len(df_invalid) > 0:
            alert_user_by_email(df_invalid)


    @task
    def save_logs(df_invalid):
        for index, row in df_invalid.iterrows():
            write_logs_to_db(index, row)


    # Task relationships
    df = read_file()
    validated_df = validate_data(df)
    invalid_df = split_file(validated_df)
    alert_errors(invalid_df)
    save_logs(invalid_df)


ingestion_dag = ingestion()
