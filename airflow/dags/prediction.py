from datetime import timedelta, datetime
import logging
import requests
import os
import pandas as pd
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.sensors.filesystem import FileSensor 
from airflow.operators.python import ShortCircuitOperator
from airflow.sensors.external_task import ExternalTaskSensor


POST_API_URL= "http://host.docker.internal:8000/predict/"


@dag(
    dag_id='predict_data',
    description='Predict a batch of data from new files',
    tags=['dsp', 'predict'],
    schedule=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=1),
    dagrun_timeout=timedelta(minutes=1)
)
def predict_every_minute_dag():

    @task()
    def merge_csv_files():
        logging.info(os.getcwd())
        folder_path = "/opt/data/folder_E"
        df_list = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and file.endswith('.csv'):
                df = pd.read_csv(file_path)
                df_list.append(df)

        merged_df = pd.concat(df_list, ignore_index=True)
        return merged_df


    @task()
    def make_predictions(merged_df):
        review_texts = merged_df["reviewText"].tolist()
        input_data = [{"review": text, "predict_type": "Job"} for text in review_texts]
        logging.info('Before calling API')
        response = requests.post(url=POST_API_URL, json=input_data)
        logging.info(f"FastAPI Response: {response.text}")


    merged_df = merge_csv_files()
    make_predictions(merged_df)


dag_instance = predict_every_minute_dag()
