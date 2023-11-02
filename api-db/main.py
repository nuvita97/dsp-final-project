# 1. Library imports
import uvicorn
from fastapi import FastAPI
import psycopg2
from classes import Rating
from functions import clean_text
from functions import tfidf
from functions import model
from functions import save_predictions

app = FastAPI()

@app.post("/predict")
def predict(data: Rating):
    review_text = data.reviewText
    cleaned_text = clean_text(review_text)
    text_vector = tfidf.transform([cleaned_text])
    rating = model.predict(text_vector)
    save_predictions(str(review_text), int(rating))
    return {"rating": rating[0]} 

@app.get('/get_predict/')
def get_predict():
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """SELECT * FROM predictions;"""
    cur.execute(sql)
    prediction = cur.fetchall()
    conn.commit()     
    cur.close()
    return prediction

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)