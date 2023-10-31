from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from main import psycopg2
# from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

# Load the trained model and TF-IDF vectorizer from the pickle file
with open("dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("dsp_tfidf.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   

# Define the text preprocessing function
def clean_text(text):
    text = str(text).lower().replace('\\', '').replace('_', ' ')
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()
    text = unidecode(text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r"(.)\\1{2,}", "\\1", text)
    return text

def save_predictions(review, rating):
    # 3. Make a connection to the database
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    # Create a cursor
    cur = conn.cursor()
    # Define the query
    sql = """INSERT INTO predictions(review, rating, timestamp) 
        VALUES('this new review', 5, NOW() ) RETURNING id;"""
    # Perform the query
    cur.execute(sql)
    # Commit and close
    conn.commit()     
    cur.close()
