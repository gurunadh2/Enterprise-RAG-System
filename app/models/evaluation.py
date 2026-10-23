from pydantic import BaseModel


class Evaluation(BaseModel):

    groundedness: float

    relevance: float