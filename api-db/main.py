from fastapi import FastAPI
import psycopg2
import pickle
from functions import Rating
from functions import clean_text, save_prediction


app = FastAPI()

# Load the trained model and TF-IDF vectorizer from the pickle file
with open("../model/dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("../model/dsp_project_tfidf_model.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   


# Predict and save predictions
@app.post("/predict/")
def predict(data: Rating):
    review_text = data.review
    cleaned_text = clean_text(review_text)
    text_vector = tfidf.transform([cleaned_text])
    rating = model.predict(text_vector)
    save_prediction(str(review_text), int(rating))
    return {"rating": rating[0]} 


# Get all predictions
@app.get('/get_predict/')
def get_predict():
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """SELECT * FROM prediction;"""
    cur.execute(sql)
    prediction = cur.fetchall()
    conn.commit()     
    cur.close()
    return prediction