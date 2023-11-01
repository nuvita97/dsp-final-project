import streamlit as st
import pandas as pd
import requests
import random
from archive.utils import random_reviews

# Create a Streamlit app
# st.title("ML Model Demo")
st.set_page_config(
    page_title="ML Legends",
    page_icon="👋",
)

st.title("Amazon Reviews Prediction")
st.sidebar.success("Select a page above.")
st.sidebar.info("Write something here...")





# Load your trained model
# with open("../model/dsp_project_model.pkl", "rb") as model_file:
#     model = pickle.load(model_file)

# Create a select box for user to choose the input method
input_choice = st.selectbox("How would you like to predict your Amazon Review?", 
                            ["Enter Text Review", "Upload CSV File"])

# Use an empty container to display content based on user choice
container = st.empty()




if input_choice == "Enter Text Review":

    # Radio button to select the situation
    situation = st.radio("Select your choice:", ("Enter your own review", "Generate random review"))

    if situation == "Enter your own review":

        # Add user input (e.g., a text box for entering a review)
        review_text = st.text_area("Enter your review:", "", height=200)

        if st.button("Predict"):

            # Prepare the data to send to the FastAPI endpoint
            input = {"review": review_text}

            # Send a POST request to the FastAPI predict endpoint
            response = requests.post(url="http://127.0.0.1:8000/predict/", json=input)

            # Check if the request was successful
            if response.status_code == 200:
                prediction = response.json()
                st.write(f"Predicted Rating: {prediction['rating']}")
            else:
                st.write("Prediction failed. Please check your input and try again.")

    else:
        
        if st.button("Generate Another Review"):
            
            generated_review = random.choice(random_reviews)
            
            review_text = st.text_area("Enter your review:", value=generated_review, height=200)
    
            # Prepare the data to send to the FastAPI endpoint
            input = {"review": review_text}

            # Send a POST request to the FastAPI predict endpoint
            response = requests.post(url="http://127.0.0.1:8000/predict/", json=input)

            # Check if the request was successful
            if response.status_code == 200:
                prediction = response.json()
                st.write(f"Predicted Rating: {prediction['rating']}")
            else:
                st.write("Prediction failed. Please check your input and try again.")


else:
    # Add file upload component
    # uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])


    # Sample data
    sample_data = {'review': ['This book is so good. Highly recommend!', 
                            'Good for reading, but nothing specical.', 
                            'This is so bad. I have never read a book this bad...']}
    sample_df = pd.DataFrame(sample_data)

    @st.cache_data
    def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(sample_df)

    st.download_button(
        label="Download sample CSV file",
        data=csv,
        file_name='sample_reviews.csv',
        mime='text/csv',
    )

    # File upload component for CSV files
    uploaded_file = container.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)

        # Add a column for predictions
        df["prediction"] = ""

        # Iterate through the rows and make predictions
        for index, row in df.iterrows():
            review_text = row["review"]

            input_data = {"review": review_text}

            response = requests.post(url="http://127.0.0.1:8000/predict/", json=input_data)

            prediction = response.json()
        
            prediction_value = prediction['rating']

            df.at[index, "prediction"] = prediction_value

        # Display the results in a table
        st.write("Prediction Result")
        st.dataframe(df[['review', 'prediction']])


    # if st.button("Predict"):
    #     if uploaded_file is not None:
    #         df = pd.read_csv(uploaded_file)
    #         input_data = {"csvData": df.to_dict(orient="records")}

    #         response = requests.post("http://localhost:8000/predict/", json=input_data)

    #         if response.status_code == 200:
    #             result = response.json()
    #             st.write(f"Predicted Rating: {result['rating']}")
    #         else:
    #             st.write("Prediction failed. Please check your input and try again.")


# else:
            
#     generated_review = random.choice(random_reviews)

#     review_text = st.text_area("Enter your review:", value=generated_review, height=200)
    
#     random_review = st.button("Generate Random Review")

#     # Prepare the data to send to the FastAPI endpoint
#     input = {"review": review_text}

#     # Send a POST request to the FastAPI predict endpoint
#     response = requests.post(url="http://127.0.0.1:8000/predict/", json=input)

#     # Check if the request was successful
#     if response.status_code == 200:
#         prediction = response.json()
#         st.write(f"Predicted Rating: {prediction['rating']}")
#     else:
#         st.write("Prediction failed. Please check your input and try again.")
