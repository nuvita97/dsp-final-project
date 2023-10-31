# 1. Library imports
import uvicorn
from fastapi import FastAPI
import psycopg2
from rating import Rating
from app import clean_text
from app import tfidf
from app import model
from app import save_predictions

# 2. Create the app object
app = FastAPI()

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, Product Owners'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/Welcome')
def get_name(name: str):
    return {'Welcome to Product Rating': f'{name}'}

@app.post("/predict")
def predict(data: Rating):
    review_text = data.reviewText

    # Clean and preprocess the input text
    cleaned_text = clean_text(review_text)

    # Transform the preprocessed text using the TF-IDF vectorizer
    text_vector = tfidf.transform([cleaned_text])

    # Predict the rating using the trained model
    rating = model.predict(text_vector)  # Use the predict method, not subscripting

    prediction_id = save_predictions(review_text, int(rating))

    return {"rating": rating[0]}  # Access the first element of the prediction


# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
#uvicorn main:app --reload