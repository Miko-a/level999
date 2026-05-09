from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest, ChatResponse, SourceDocument
from app.services.vector_store_service import (
    search_similar_chunks,
    build_context_from_chunks,
)
from app.services.prompt_service import build_rag_prompt
from app.services.gemini_service import ask_gemini

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        print("Received message:", request.message)

        relevant_chunks = search_similar_chunks(
            query=request.message,
            top_k=5,
        )

        context = build_context_from_chunks(relevant_chunks)

        prompt = build_rag_prompt(
            user_message=request.message,
            context=context,
        )

        answer = ask_gemini(
            user_message=request.message,
            prompt=prompt,
            context=context,
        )

        sources = [
            SourceDocument(
                title=chunk["title"],
                source_id=chunk["source_id"],
                file_name=chunk["file_name"],
                chunk_id=chunk["chunk_id"],
                category=chunk["category"],
                topic=chunk["topic"],
                version=chunk["version"],
                score=chunk["score"],
                preview=chunk["preview"],
            )
            for chunk in relevant_chunks
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))