from datetime import timedelta
import os
import glob
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
import ge_valid as ge


@dag(
    dag_id="validate_data",
    description="Validate data from a file to agreat_expectations initnother DAG",
    tags=["dsp", "validation"],
    schedule=timedelta(minutes=1),
    start_date=days_ago(n=0, hour=0),
)
def validate_data():
    @task
    def get_validation() -> None:
        input = ("data/folder_A")
        output_success = ("data/folder_C")
        output_fail = ("data/folder_B")
        file_pattern = os.path.join(input, "*.csv")
        file_paths = glob.glob(file_pattern)

        for file_path in file_paths:
            ge.process_file(file_path, output_fail, output_success)

    get_validation()

validate_data_dag = validate_data()
