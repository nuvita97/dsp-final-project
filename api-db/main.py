from fastapi import FastAPI, UploadFile
import psycopg2
import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer
from classes import Rating, Prediction
from functions import clean_text, save_prediction


app = FastAPI()

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

    # Store the prediction
    save_prediction(str(review_text), int(rating))

    return {"rating": rating[0]}  # Access the first element of the prediction

# @app.post("/predict_csv/")
# def predict_csv(file: UploadFile):
#     return {"rating": 0}


# Get all predictions
@app.get('/get_predict/')
def get_predict():
    # Make a connection to the database
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    # Create a cursor
    cur = conn.cursor()
    # Define the query
    sql = """SELECT * FROM prediction;"""
    # Perform the query
    cur.execute(sql)
    # Get the predictions
    prediction = cur.fetchall()
    # Commit and close
    conn.commit()     
    cur.close()
    # Return the predictions
    return prediction