from fastapi import FastAPI
import psycopg2
import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer
from classes import Rating, Prediction
from functions import clean_text

app = FastAPI()

# Make a connection to the database
conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
# Create a cursor
cur = conn.cursor()
# Define the query
sql = """INSERT INTO inputs(image)
        VALUES('this is test') RETURNING id;"""
# Perform the query
cur.execute(sql)
# Commit and close
conn.commit()     
cur.close()


# Load the trained model and TF-IDF vectorizer from the pickle file
with open("../model/dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("../model/dsp_tfidf.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   


@app.post("/predict/")
def predict(data: Rating):
    review_text = data.review

    # Clean and preprocess the input text
    cleaned_text = clean_text(review_text)

    # Transform the preprocessed text using the TF-IDF vectorizer
    text_vector = tfidf.transform([cleaned_text])

    # Predict the rating using the trained model
    rating = model.predict(text_vector)  # Use the predict method, not subscripting

    return {"rating": rating[0]}  # Access the first element of the prediction
