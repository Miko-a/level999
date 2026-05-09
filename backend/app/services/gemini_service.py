import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"


def ask_mock_llm(user_message: str, context: str) -> str:
    if not context.strip():
        return f"""
Aku menerima pertanyaan kamu:

"{user_message}"

Namun knowledge base lokal belum memiliki dokumen yang cukup relevan untuk menjawab pertanyaan ini.

Karena saat ini backend berjalan dalam mock mode, aku tidak akan mengarang jawaban di luar knowledge base.

Saran:
- Tambahkan dokumen baru ke folder backend/app/knowledge.
- Pastikan dokumen mengandung kata kunci yang sesuai dengan pertanyaan user.
"""

    return f"""
Jawaban mock berbasis knowledge base lokal.

Pertanyaan:
"{user_message}"

Berdasarkan dokumen yang ditemukan, berikut jawaban yang aman untuk Phase 2:

{extract_simple_answer_from_context(context)}

Catatan:
- Ini adalah mock response karena Gemini sedang tidak dipakai.
- Retrieval lokal sudah berjalan.
- Jawaban ini belum memakai embedding/vector database.
- Akurasi masih bergantung pada isi file Markdown di folder knowledge.
"""


def extract_simple_answer_from_context(context: str) -> str:
    lines = []

    for line in context.splitlines():
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.startswith("#"):
            continue

        if clean_line.lower().startswith("source id:"):
            continue

        if clean_line.lower().startswith("topic:"):
            continue

        if clean_line.lower().startswith("game:"):
            continue

        if clean_line.lower().startswith("version:"):
            continue

        if clean_line.lower().startswith("[document"):
            continue

        if clean_line.lower().startswith("title:"):
            continue

        if clean_line.lower().startswith("file:"):
            continue

        if clean_line.lower().startswith("content:"):
            continue

        lines.append(clean_line)

        if len(lines) >= 8:
            break

    if not lines:
        return "Dokumen relevan ditemukan, tetapi tidak ada ringkasan yang bisa dibuat."

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