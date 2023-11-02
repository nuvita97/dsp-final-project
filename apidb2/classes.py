from pydantic import BaseModel


class Rating(BaseModel):
    review: str

class Prediction(BaseModel):
    rating: float
