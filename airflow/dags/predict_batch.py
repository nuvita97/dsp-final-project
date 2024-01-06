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


POST_API_URL = "http://localhost:8000/predict/"
GET_API_URL = "http://localhost:8000/get_predict/"

@dag(
    dag_id='predict_data',
    description='Predict a batch of data from new files',
    tags=['dsp', 'predict'],
    schedule=timedelta(minutes=2),
    start_date=days_ago(n=0, hour=1),
    dagrun_timeout=timedelta(minutes=1)
)
def predict_every_minute_dag():

    # check_for_files = ShortCircuitOperator(
    #     task_id='check_for_files',
    #     python_callable=check_for_new_files,
    # )

    # wait_for_new_files = FileSensor(
    #     task_id='wait_for_new_files',
    #     mode='reschedule',
    #     timeout=600,  # Adjust as needed
    #     filepath="data/folder_C",
    #     soft_fail=True,  
    # )

    @task()
    def merge_csv_files():
        folder_path = "data/folder_C"
        df_list = []

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path) and file.endswith('.csv'):
                df = pd.read_csv(file_path)
                df_list.append(df)

        merged_df = pd.concat(df_list, ignore_index=True)
        return merged_df


    # @task()
    # def make_predictions(merged_df):
    #     review_texts = merged_df["reviewText"].tolist()
    #     input_data = [{"review": text} for text in review_texts]
    #     logging.info('Before calling API')
    #     try:
    #         response = requests.post(url=POST_API_URL, json=input_data)
    #         logging.info(f"FastAPI Response: {response.text}")
    #     except Exception as e:
    #         logging.error(f"Error calling FastAPI: {str(e)}")
    #         raise

    @task
    def get_predictions():
        response = requests.get(GET_API_URL)
        columns_list = ["ID", "Review", "Rating Prediction", "Predict Time", "Predict Type"]
        df = pd.DataFrame(response, columns=columns_list)
        df.to_csv('data/folder_B/test_get_predict_files.csv')


    merged_df = merge_csv_files()
    # make_predictions(merged_df)
    get_predictions()

    # merged_df >> make_predictions_task
    # wait_for_new_files >> merge_csv_files() >> save_data(merged_df)

# Instantiate the DAG
dag_instance = predict_every_minute_dag()


