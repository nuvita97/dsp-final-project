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
        predict_type = data[i].predict_type
        save_prediction(str(review_text), rating, predict_type)
        predictions.append({"review": review_text, "rating": rating, "predict_type": predict_type})

    return {"predictions": predictions}


# Get predictions with filters
@app.get('/get_filtered_predict/')
def get_filtered_predict(
    start_date: str = Query(None),
    end_date: str = Query(None),
    start_time: str = Query(None),
    end_time: str = Query(None),
    selected_ratings: list = Query(None),
    selected_types: list = Query(None)
):
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()

    sql = """SELECT * FROM prediction WHERE 1=1"""

    # Add filters based on parameters
    if start_date:
        sql += f" AND time >= '{start_date} {start_time or '00:00:00'}'"
    if end_date:
        sql += f" AND time <= '{end_date} {end_time or '23:59:59'}'"
    if selected_ratings:
        sql += f" AND rating IN ({', '.join(map(str, selected_ratings))})"
    if selected_types:
        sql += f" AND type IN ({', '.join(map(lambda x: f'{x!r}', selected_types))})"

    sql += " ORDER BY id;"

    cur.execute(sql)
    predictions = cur.fetchall()

    conn.commit()
    cur.close()
    
    return predictions


# Get all predictions
# @app.get('/get_predict/')
# def get_predict():
#     conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
#     cur = conn.cursor()
#     sql = """SELECT * FROM prediction ORDER BY id;"""
#     cur.execute(sql)
#     prediction = cur.fetchall()
#     conn.commit()     
#     cur.close()
#     return prediction