import streamlit as st
import pandas as pd
import requests


st.title("Predictions History")
st.sidebar.success("Select a page above.")


# Make an API GET request
response = requests.get(url='http://127.0.0.1:8000/get_predict/')

# Check the response status code
if response.status_code == 200:
    # Successful response
    data = response.json()  # Assuming the API returns JSON data

    columns_list = ["ID", "Review", "Rating", "Predict Time"]
    # data.insert(0, columns_list)

    df = pd.DataFrame(data, columns=columns_list)
    df = df.set_index(df.columns[0])
    # df = df.set_index(df.)

    # Display the API data in a Streamlit table
    st.table(df)
else:
    # Handle error if the API request fails
    st.error(f"API request failed with status code {response.status_code}")


