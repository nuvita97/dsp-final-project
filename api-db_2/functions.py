from bs4 import BeautifulSoup
from unidecode import unidecode
import re
import requests
import psycopg2


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


# Store a prediction
def save_prediction(review, rating):
    # Make a connection to the database
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    # Create a cursor
    cur = conn.cursor()
    # Define the query
    sql = """INSERT INTO prediction (review, rating, time, type)
                VALUES(%s, %s, now(), %s) RETURNING id;"""
    # Perform the query
    cur.execute(sql, (review, rating, 'App'))
    # Get the prediction id
    cur.fetchone()[0]
    # Commit and close
    conn.commit()     
    cur.close()
    # Return the prediction id

    # return prediction_id


