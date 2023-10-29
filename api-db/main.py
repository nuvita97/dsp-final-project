from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from bs4 import BeautifulSoup
from unidecode import unidecode
import re
from sklearn.feature_extraction.text import TfidfVectorizer

app = FastAPI()

# Load the trained model and TF-IDF vectorizer from the pickle file
with open("dsp_project_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("dsp_tfidf.pkl", "rb") as model_file:
    tfidf = pickle.load(model_file)   


class Rating(BaseModel):
    review: str

class PredictionResult(BaseModel):
    rating: float

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

@app.post("/predict/")
def predict(data: Rating):
    review_text = data.review

    # Clean and preprocess the input text
    cleaned_text = clean_text(review_text)

    # Transform the preprocessed text using the TF-IDF vectorizer
    text_vector = tfidf.transform([cleaned_text])

    # Predict the rating using the trained model
    rating = model.predict(text_vector)  # Use the predict method, not subscripting

    return {"rating": rating[0]}  # Access the first element of the prediction
