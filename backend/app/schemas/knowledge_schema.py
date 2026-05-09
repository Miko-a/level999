from pydantic import BaseModel
from typing import List


class KnowledgeFile(BaseModel):
    file_name: str
    title: str
    source_id: str
    category: str
    topic: str
    version: str
    size: int


class KnowledgeListResponse(BaseModel):
    files: List[KnowledgeFile]


class CreateKnowledgeRequest(BaseModel):
    file_name: str
    title: str
    source_id: str
    category: str
    topic: str
    version: str = "internal-demo"
    tags: str = ""
    content: str


class CreateKnowledgeResponse(BaseModel):
    message: str
    file_name: str


class DeleteKnowledgeResponse(BaseModel):
    message: str
    file_name: str


class ReingestResponse(BaseModel):
    message: str
    chunk_count: int


class VectorStatsResponse(BaseModel):
    collection_name: str
    chunk_count: int