from bs4 import BeautifulSoup
from unidecode import unidecode
from pydantic import BaseModel
import re
import psycopg2


class Rating(BaseModel):
    review: str
    

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
    text = text.replace("'", '')
    text = text.replace('"', '')  
    return text


# Store prediction into DB
def save_prediction(review, rating):
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    cur = conn.cursor()
    sql = """INSERT INTO prediction (review, rating, time, type)
                VALUES(%s, %s, now(), %s) RETURNING id;"""
    cur.execute(sql, (review, rating, 'App'))
    cur.fetchone()[0]
    conn.commit()     
    cur.close()
