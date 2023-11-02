from pydantic import BaseModel


class Rating(BaseModel):
    review: str

