import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"


def ask_mock_llm(user_message: str) -> str:
    return f"""
Ini adalah jawaban mock dari backend.

Pertanyaan kamu:
"{user_message}"

Karena rate limit Gemini sedang habis, backend memakai mock response untuk sementara.
"""


def ask_gemini(user_message: str) -> str:
    try:
        if USE_MOCK_LLM:
            return ask_mock_llm(user_message)

        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY is not set in .env")

        client = genai.Client(api_key=GEMINI_API_KEY)

        system_instruction = """
You are an assistant for Honkai: Star Rail players.

Your role:
- Help beginners understand basic game concepts.
- Give practical guidance about characters, teams, relics, light cones, and farming priorities.
- Be honest when you are unsure.
- Do not claim that your answer is based on the latest patch unless patch data is provided.
- Keep answers clear and structured.

Important limitation:
This version does not use a RAG knowledge base yet.
If the question needs exact current meta, latest patch data, or exact numbers, say that the data should be verified.
"""

        prompt = f"""
{system_instruction}

User question:
{user_message}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text or "I could not generate an answer."
    except Exception as e:
        print(f"An error occurred in ask_gemini: {e}")
        raise e