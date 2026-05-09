from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    message: str


class SourceDocument(BaseModel):
    title: str
    source_id: str
    file_name: str
    chunk_id: str
    category: str
    topic: str
    version: str
    score: float
    preview: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]