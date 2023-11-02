import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
from archive.utils import convert_time_format


API_URL = "http://127.0.0.1:8000/get_predict/"


st.title("Predictions History")
st.sidebar.success("Select a page above.")



# Make an API GET request
response = requests.get(url=API_URL)

# Successful response
data = response.json()  # Assuming the API returns JSON data

columns_list = ["ID", "Review", "Rating Prediction", "Predict Time", "Predict Type"]
# data.insert(0, columns_list)

df = pd.DataFrame(data, columns=columns_list)
df = df.set_index(df.columns[0])
# df = df.set_index(df.)

# Apply the function to the "Predict Time" column
df["Predict Time"] = df["Predict Time"].apply(convert_time_format)
df["Predict Time"] = pd.to_datetime(df["Predict Time"])


# Calculate the default start date (3 days ago)
default_start_date = datetime.now() - timedelta(days=3)
default_end_time = datetime.now() + timedelta(minutes=2)

# Create a two-column layout
col1, col2 = st.columns(2)

# Left column for start_date and start_time
with col1:
    start_date = st.date_input("Start Date", default_start_date)
    start_time = st.time_input("Start Time")

# Right column for end_date and end_time
with col2:
    end_date = st.date_input("End Date", pd.Timestamp.now().date())
    end_time = st.time_input("End Time", default_end_time)


# Sidebar widgets for time filter
# start_datetime = st.datetime_input("Start Date and Time", default_start_date)
# end_datetime = st.datetime_input("End Date and Time", pd.Timestamp.now())



# Check the response status code
if response.status_code == 200:
    # Filter data based on the selected time range
    filtered_df = df[(df["Predict Time"] >= pd.to_datetime(start_date.strftime("%Y-%m-%d") + " " + start_time.strftime("%H:%M:%S")))
                    & (df["Predict Time"] <= pd.to_datetime(end_date.strftime("%Y-%m-%d") + " " + end_time.strftime("%H:%M:%S")))]

    # Display the filtered data
    st.write("Filtered Data:")
    st.table(filtered_df)

else:
    # Handle error if the API request fails
    st.error(f"API request failed with status code {response.status_code}")


