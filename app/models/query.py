from typing import List
from typing import Optional

from pydantic import BaseModel

from app.models.citation import Citation
from app.models.evaluation import Evaluation


class QueryRequest(BaseModel):

    question: str

    source_filter: Optional[List[str]] = None


class QueryResponse(BaseModel):

    answer: str

    sources: List[Citation]

    evaluation: Evaluation