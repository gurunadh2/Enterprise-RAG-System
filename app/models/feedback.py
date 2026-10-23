from pydantic import BaseModel


class FeedbackRequest(BaseModel):

    question: str

    answer: str

    rating: str