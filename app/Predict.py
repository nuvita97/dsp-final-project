import streamlit as st
import pandas as pd
import requests
import random
from archive.utils import random_reviews, predict_comment


POST_API_URL = "http://127.0.0.1:8000/predict/"


st.set_page_config(
    page_title="ML Legends",
    page_icon="🤖",
    layout="wide"
)

st.title("📖 Kindle Reviews Prediction")
st.sidebar.info("📄 In this page, we will predict the Overall Rating of a Kindle book based on reviews of Amazon users.")
st.sidebar.write("© A product of ML Legends")


input_choice = st.selectbox("🧐 How would you like to predict your Amazon Review?", 
                            ["Enter Text Review", "Upload CSV File"])


container = st.empty()


if input_choice == "Enter Text Review":

    situation = st.radio("🔽 Select your choice:", ("Enter your own review", "Generate random review"))

    if situation == "Enter your own review":

        review_text = st.text_area("✏️ Enter your review:", "", height=200)

        if st.button("🔎 Predict"):

            input = {"review": review_text}

            response = requests.post(url=POST_API_URL, json=input)

            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Predicted Rating: {prediction['rating']}")
            else:
                st.write("Prediction failed. Please check your input and try again.")

            predict_comment(prediction['rating'])

    else:
        
        if st.button("Generate Another Review"):
            
            generated_review = random.choice(random_reviews)
            
            review_text = st.text_area("Enter your review:", value=generated_review, height=200)
    
            input = {"review": review_text}

            response = requests.post(url=POST_API_URL, json=input)

            if response.status_code == 200:
                prediction = response.json()
                st.success(f"Predicted Rating: {prediction['rating']}")
            else:
                st.write("Prediction failed. Please check your input and try again.")

            predict_comment(prediction['rating'])
            

else:

    sample_data = {'review': ['This book is so good. Highly recommend!', 
                            'Good for reading, but nothing specical.', 
                            'This is so bad. I have never read a book this bad...']}
    sample_df = pd.DataFrame(sample_data)

    @st.cache_data
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(sample_df)

    st.download_button(
        label="💾 Download sample CSV file",
        data=csv,
        file_name='sample_reviews.csv',
        mime='text/csv',
    )

    uploaded_file = st.file_uploader("📤 Upload your CSV file here, recommended to use the sample file above.", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df["prediction"] = ""

        for index, row in df.iterrows():
            review_text = row["review"]

            input_data = {"review": review_text}

            response = requests.post(url=POST_API_URL, json=input_data)

            prediction = response.json()
        
            prediction_value = prediction['rating']

            df.at[index, "prediction"] = prediction_value

        st.write("🖨️ Prediction Result")
        st.dataframe(df[['review', 'prediction']])

