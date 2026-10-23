from pydantic import BaseModel


class Citation(BaseModel):

    file: str

    chunk_id: int

    text: str