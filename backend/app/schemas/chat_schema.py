from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    message: str


class SourceDocument(BaseModel):
    title: str
    source_id: str
    file_name: str
    score: int
    preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]