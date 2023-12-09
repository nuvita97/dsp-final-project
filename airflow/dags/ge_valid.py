import logging
import great_expectations as ge
import shutil
import os
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class DataProblemsStatistics(Base):
    __tablename__ = "data_problems_statistics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String)
    column = Column(String)
    expectation_values = Column(String)
    unexpected_values = Column(Text)
    date_validation = Column(Date)


def read_and_validate_file(df):
    context = ge.DataContext("gx")
    expectation_suite_name = "external.table.warning"
    suite = context.get_expectation_suite(expectation_suite_name)

    if suite is None:
        suite = context.create_expectation_suite(expectation_suite_name)

    ge_df = ge.dataset.PandasDataset(df, expectation_suite=suite)

    # VALIDATION 1
    ge_df.expect_column_values_to_not_be_null('reviewText')

    validation_result = ge_df.validate()

    return validation_result


def process_file(file_path, folder_b, folder_c):
    db_url = "postgresql://postgres:password@172.21.112.1/amazon-reviews"
    df = pd.read_csv(file_path)
    validation_result = read_and_validate_file(df)

    if validation_result["success"]:
        store_file_in_folder(file_path, folder_c)
    else:
        store_file_in_folder(file_path, folder_b)

        # save_data_problems_statistics(validation_result, file_path, db_url)


def store_file_in_folder(file_path, destination_folder):
    shutil.move(
        file_path,
        os.path.join(destination_folder, os.path.basename(file_path)),
    )


def save_data_problems_statistics(validation_result, file_path, db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info(f"{validation_result}")

    for result in validation_result["results"]:
        if not result["success"]:
            column = result["expectation_config"]["kwargs"]["column"]
            expectation_values = result["expectation_config"]["kwargs"][
                "value_set"
            ]
            unexpected_values = str(
                result["result"]["partial_unexpected_list"]
            )

            stat = DataProblemsStatistics(
                file_name=file_path,
                column=column,
                expectation_values=expectation_values,
                unexpected_values=unexpected_values,
                date_validation=datetime.now().strftime("%Y-%m-%d"),
            )
            session.add(stat)

    session.commit()
    session.close()


def split_file_and_save_problems(file_path, folder_b, folder_c, validation_result, db_url):
    df = pd.read_csv(file_path)

    problematic_rows = []
    for result in validation_result["results"]:
        if not result["success"]:
            problematic_rows.extend(result["result"]["unexpected_index_list"])

    if problematic_rows:
        df_problems = df.loc[problematic_rows]
        df_no_problems = df.drop(problematic_rows)

        # save_data_problems_statistics(validation_result, db_url)

        problems_file_path = os.path.join(
            folder_b, f"file_with_data_problems_{os.path.basename(file_path)}"
        )
        df_problems.to_csv(problems_file_path, index=False)

        no_problems_file_path = os.path.join(
            folder_c,
            f"file_without_data_problems_{os.path.basename(file_path)}",
        )
        df_no_problems.to_csv(no_problems_file_path, index=False)

    else:
        store_file_in_folder(file_path, folder_c)