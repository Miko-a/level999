import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.chat import router as chat_router
from app.routes.knowledge import router as knowledge_router

app = FastAPI(
    title="HSR RAG Chatbot Backend",
    description="FastAPI backend for Honkai: Star Rail chatbot using Gemini API.",
    version="0.1.0",
)

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
)

allowed_origins = [
    origin.strip()
    for origin in FRONTEND_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(knowledge_router)


@app.get("/")
def root():
    return {
        "message": "HSR RAG Chatbot Backend is running."
    }




