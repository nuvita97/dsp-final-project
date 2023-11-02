from fastapi import FastAPI
import pickle
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from main import psycopg2

app = FastAPI()
with open("dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("dsp_tfidf.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   

def clean_text(text):
    text = str(text).lower().replace('\\', '').replace('_', ' ')
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = unidecode(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r"(.)\\1{2,}", "\\1", text)
    text = text.replace("'", '')
    text = text.replace('"', '') 
    return text

def save_predictions(review, rating):
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """INSERT INTO predictions(review, rating, time, type) 
        VALUES(%s, %s, now(), %s) RETURNING id;"""
    cur.execute(sql, (review, rating, 'job'))
    cur.fetchone()[0]
    conn.commit()     
    cur.close()
