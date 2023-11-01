from bs4 import BeautifulSoup
from unidecode import unidecode
import re
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
    sql = """INSERT INTO prediction (review, rating, time)
                VALUES(%s, %s, now()) RETURNING id;"""
    # Perform the query
    cur.execute(sql, (review, rating))
    # Get the prediction id
    prediction_id = cur.fetchone()[0]
    # Commit and close
    conn.commit()     
    cur.close()
    # Return the prediction id
    return prediction_id


def get_prediction():
    # Make a connection to the database
    conn = psycopg2.connect("dbname=amazon-reviews user=postgres password=password")
    # Create a cursor
    cur = conn.cursor()
    # Define the query
    sql = """SELECT * FROM prediction ORDER BY id DESC;"""
    # Perform the query
    cur.execute(sql)
    # Get the predictions
    prediction = cur.fetchall()
    # Commit and close
    conn.commit()     
    cur.close()
    # Return the predictions
    return prediction