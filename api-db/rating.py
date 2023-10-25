from pydantic import BaseModel
# 1. Class which describes the review text
class Rating(BaseModel):
    reviewText: str 
    # overall: int