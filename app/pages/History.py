import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from archive.utils import convert_time_format


GET_API_URL = "http://127.0.0.1:8000/get_predict/"

st.set_page_config(
    page_title="ML Legends",
    page_icon="🤖",
    layout="wide"
)

st.title("🕰️  Predictions History")
st.sidebar.info("📄 In this page, we will show all the filtered prediction history.")
st.sidebar.write("© A product of ML Legends")


response = requests.get(url=GET_API_URL)

data = response.json()

columns_list = ["ID", "Review", "Rating Prediction", "Predict Time", "Predict Type"]

df = pd.DataFrame(data, columns=columns_list)
df = df.set_index(df.columns[0])

df["Predict Time"] = df["Predict Time"].apply(convert_time_format)
df["Predict Time"] = pd.to_datetime(df["Predict Time"])


# Calculate the default start date & end time
default_start_date = datetime.now() - timedelta(days=3)
default_end_time = datetime.now() + timedelta(minutes=2)

col1, col2 = st.columns(2)

# Left column for start_date and start_time
with col1:
    start_date = st.date_input("Start Date", default_start_date)
    start_time = st.time_input("Start Time")

# Right column for end_date and end_time
with col2:
    end_date = st.date_input("End Date", pd.Timestamp.now().date())
    end_time = st.time_input("End Time", default_end_time)

# 2 columns for filter Ratings & Type
col3, col4 = st.columns(2)

with col3:
    unique_ratings = [1, 2, 3, 4, 5]
    selected_ratings = st.multiselect('Select Ratings to Filter', unique_ratings, default=unique_ratings)

with col4:
    unique_types = ['App', 'Job']
    selected_types = st.multiselect('Select Prediction Type to Filter', unique_types, default=unique_types)



if response.status_code == 200:
    filtered_df = df[(df["Predict Time"] >= pd.to_datetime(start_date.strftime("%Y-%m-%d") + " " + start_time.strftime("%H:%M:%S")))
                    & (df["Predict Time"] <= pd.to_datetime(end_date.strftime("%Y-%m-%d") + " " + end_time.strftime("%H:%M:%S")))]

    # Filter the data based on selected ratings or show all data if none selected
    if selected_ratings:
        filtered_df = filtered_df[filtered_df['Rating Prediction'].isin(selected_ratings)]

    # Filter the data based on selected ratings or show all data if none selected
    if selected_ratings:
        filtered_df = filtered_df[filtered_df['Predict Type'].isin(unique_types)]

    st.write("Filtered Data")
    st.table(filtered_df)

else:
    st.error(f"API request failed with status code {response.status_code}")


