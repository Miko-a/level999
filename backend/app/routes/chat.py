from fastapi import APIRouter, HTTPException

from app.schemas.chat_schema import ChatRequest, ChatResponse, SourceDocument
from app.services.retriever_service import (
    retrieve_relevant_documents,
    build_context_from_documents,
)
from app.services.prompt_service import build_rag_prompt
from app.services.gemini_service import ask_gemini

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        print("Received message:", request.message)

        relevant_documents = retrieve_relevant_documents(
            query=request.message,
            top_k=3,
        )

        context = build_context_from_documents(relevant_documents)

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
                title=document["title"],
                source_id=document["source_id"],
                file_name=document["file_name"],
                score=document["score"],
                preview=document["preview"],
            )
            for document in relevant_documents
        ]

        return ChatResponse(
            answer=answer,
            sources=sources,
        )

    except Exception as error:
        print("ERROR:", repr(error))
        raise HTTPException(status_code=500, detail=str(error))