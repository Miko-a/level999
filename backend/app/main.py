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

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "https://level999-jet.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        FRONTEND_ORIGIN,
        "https://level999-jet.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=False,
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