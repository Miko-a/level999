import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"


def ask_mock_llm(user_message: str, context: str) -> str:
    if not context.strip():
        return f"""
Knowledge base lokal belum memiliki konteks yang cukup relevan untuk menjawab pertanyaan ini.

Pertanyaan:
"{user_message}"

Saran:
- Tambahkan dokumen baru ke folder backend/app/knowledge.
- Jalankan ulang ingestion dengan perintah: python -m app.scripts.ingest_knowledge
- Pastikan dokumen memiliki metadata seperti Source ID, Category, Topic, Version, dan Tags.
"""

    return f"""
Berdasarkan knowledge base lokal, berikut jawaban yang aman:

{extract_simple_answer_from_context(context)}

Catatan:
- Jawaban ini berasal dari mock LLM.
- Retrieval sudah memakai vector database lokal.
- Knowledge base masih bersifat internal-demo.
- Jangan gunakan jawaban ini sebagai klaim patch/meta terbaru.
"""


def extract_simple_answer_from_context(context: str) -> str:
    lines = []

    skipped_prefixes = (
        "#",
        "source id:",
        "category:",
        "topic:",
        "game:",
        "version:",
        "tags:",
        "[source",
        "title:",
        "file:",
        "chunk id:",
        "similarity score:",
        "content:",
    )

    for line in context.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()

        if lower_line.startswith(skipped_prefixes):
            continue

        lines.append(clean_line)

        if len(lines) >= 10:
            break

    if not lines:
        return "Dokumen relevan ditemukan, tetapi tidak ada isi yang bisa diringkas."

    return "\n".join(f"- {line}" for line in lines)


def ask_gemini(user_message: str, prompt: str, context: str) -> str:
    if USE_MOCK_LLM:
        return ask_mock_llm(user_message=user_message, context=context)

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in .env")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text or "I could not generate an answer."