from fastapi import APIRouter, HTTPException
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.gemini_service import ask_gemini

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = ask_gemini(request.message)
        return ChatResponse(answer=answer)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))