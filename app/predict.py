import streamlit as st
import requests
import json
import pickle
import random
from archive.random import random_reviews

# Create a Streamlit app
# st.title("ML Model Demo")
st.set_page_config(
    page_title="ML Legends",
    page_icon="👋",
)

st.title("Amazon Reviews Prediction")
st.sidebar.success("Select a page above.")


# Load your trained model
with open("../model/dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Create a select box for user to choose the input method
input_choice = st.selectbox("How would you like to predict your Amazon Review?", 
                            ["Enter Text Review", "Upload CSV File"])

# Use an empty container to display content based on user choice
container = st.empty()




if input_choice == "Enter Text Review":

# Add user input (e.g., a text box for entering a review)
    
    random_review = st.button("Generate Random Review")
    
    
    if random_review:
        generated_review = random.choice(random_reviews)

        review_text = st.text_area("Enter your review:", value=generated_review)

    else:
        review_text = st.text_area("Enter your review:")

    # # Create a "Clear Text" button
    # if st.button("Clear Text"):
    #     # Clear the content of the text_review text area
    #     review_text.empty()
    
    if st.button("Predict"):
        

        # Prepare the data to send to the FastAPI endpoint
        input = {"review": review_text}

        # Send a POST request to the FastAPI predict endpoint
        response = requests.post(url="http://localhost:8000/predict/", json=input)

        # Check if the request was successful
        if response.status_code == 200:
            prediction = response.json()
            st.write(f"Predicted Rating: {prediction['rating']}")
        else:
            st.write("Prediction failed. Please check your input and try again.")

elif input_choice == "Upload CSV File":
    # Add file upload component
    # uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    # File upload component for CSV files
    uploaded_file = container.file_uploader("Upload a CSV file", type=["csv"])

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
