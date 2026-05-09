from fastapi import APIRouter, HTTPException

from app.schemas.knowledge_schema import (
    KnowledgeListResponse,
    CreateKnowledgeRequest,
    CreateKnowledgeResponse,
    DeleteKnowledgeResponse,
    ReingestResponse,
    VectorStatsResponse,
)
from app.services.knowledge_service import (
    list_knowledge_files,
    create_knowledge_file,
    delete_knowledge_file,
)
from app.services.vector_store_service import get_vector_stats
from app.scripts.ingest_knowledge import ingest_knowledge


router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


@router.get("", response_model=KnowledgeListResponse)
def list_files():
    try:
        files = list_knowledge_files()
        return KnowledgeListResponse(files=files)

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))


@router.post("", response_model=CreateKnowledgeResponse)
def create_file(request: CreateKnowledgeRequest):
    try:
        result = create_knowledge_file(
            file_name=request.file_name,
            title=request.title,
            source_id=request.source_id,
            category=request.category,
            topic=request.topic,
            version=request.version,
            tags=request.tags,
            content=request.content,
        )

        return CreateKnowledgeResponse(
            message="Knowledge file created successfully.",
            file_name=result["file_name"],
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))


@router.delete("/{file_name}", response_model=DeleteKnowledgeResponse)
def delete_file(file_name: str):
    try:
        result = delete_knowledge_file(file_name)

        return DeleteKnowledgeResponse(
            message="Knowledge file deleted successfully.",
            file_name=result["file_name"],
        )

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error))

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))


@router.post("/reingest", response_model=ReingestResponse)
def reingest():
    try:
        chunk_count = ingest_knowledge()

        return ReingestResponse(
            message="Knowledge base re-ingested successfully.",
            chunk_count=chunk_count,
        )

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))


@router.get("/stats", response_model=VectorStatsResponse)
def stats():
    try:
        result = get_vector_stats()

        return VectorStatsResponse(
            collection_name=result["collection_name"],
            chunk_count=result["chunk_count"],
        )

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))