from fastapi import FastAPI, Query
import psycopg2
import pickle
from functions import Rating
from functions import clean_text, save_prediction
from typing import List


app = FastAPI()

# Load the trained model and TF-IDF vectorizer from the pickle file
with open("../model/dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("../model/dsp_project_tfidf_model.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   


# Predict and save predictions
@app.post("/predict/")
def predict(data: List[Rating]):

    reviews = [clean_text(d.review) for d in data]
    text_vectors = tfidf.transform(reviews)
    ratings = model.predict(text_vectors)

    predictions = []
    for i in range(len(data)):
        review_text = data[i].review
        rating = int(ratings[i])
        save_prediction(str(review_text), rating)
        predictions.append({"review": review_text, "rating": rating})

    return {"predictions": predictions}


# Get all predictions
@app.get('/get_predict/')
def get_predict():
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """SELECT * FROM prediction ORDER BY id;"""
    cur.execute(sql)
    prediction = cur.fetchall()
    conn.commit()     
    cur.close()
    return prediction