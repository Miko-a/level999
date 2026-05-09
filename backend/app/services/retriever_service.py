from pathlib import Path
import re
from typing import List, Dict


KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"


QUERY_EXPANSIONS = {
    "hsr": ["honkai", "star", "rail"],
    "relic": ["relic", "relics"],
    "relics": ["relic", "relics"],
    "elemen": ["element", "elements", "elemen"],
    "element": ["element", "elements", "elemen"],
    "path": ["path", "paths"],
    "team": ["team", "teams", "tim"],
    "tim": ["team", "teams", "tim"],
    "farming": ["farming", "farm"],
    "farm": ["farming", "farm"],
    "beginner": ["beginner", "pemula", "new"],
    "pemula": ["beginner", "pemula", "new"],
    "build": ["build", "building"],
    "healer": ["healer", "healing", "abundance", "sustain"],
    "shield": ["shield", "shielder", "preservation", "sustain"],
    "dps": ["dps", "damage", "damage dealer"],
}


STOPWORDS = {
    "apa",
    "itu",
    "di",
    "ke",
    "dari",
    "yang",
    "dan",
    "atau",
    "untuk",
    "dengan",
    "bagaimana",
    "cara",
    "adalah",
    "the",
    "a",
    "an",
    "is",
    "are",
    "in",
    "on",
    "of",
    "to",
    "for",
    "and",
    "or",
}


def normalize_text(text: str) -> str:
    return text.lower().strip()


def tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    return re.findall(r"[a-zA-Z0-9]+", text)


def expand_query_tokens(tokens: List[str]) -> List[str]:
    expanded_tokens = []

    for token in tokens:
        if token in STOPWORDS:
            continue

        expanded_tokens.append(token)

        if token in QUERY_EXPANSIONS:
            expanded_tokens.extend(QUERY_EXPANSIONS[token])

        if token.endswith("s") and len(token) > 3:
            expanded_tokens.append(token[:-1])

    return list(set(expanded_tokens))


def read_knowledge_files() -> List[Dict]:
    documents = []

    if not KNOWLEDGE_DIR.exists():
        print("Knowledge directory does not exist:", KNOWLEDGE_DIR)
        return documents

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        title = file_path.stem.replace("-", " ").title()
        source_id = file_path.stem

        for line in content.splitlines():
            if line.lower().startswith("source id:"):
                source_id = line.split(":", 1)[1].strip()

            if line.startswith("# "):
                title = line.replace("# ", "").strip()

        documents.append(
            {
                "title": title,
                "source_id": source_id,
                "file_name": file_path.name,
                "content": content,
            }
        )

    print(f"Loaded {len(documents)} knowledge documents from {KNOWLEDGE_DIR}")

    return documents


def score_document(query: str, document: Dict) -> int:
    query_tokens = tokenize(query)
    expanded_query_tokens = expand_query_tokens(query_tokens)

    content = document["content"]
    title = document["title"]
    file_name = document["file_name"]

    searchable_text = f"{title}\n{file_name}\n{content}"

    content_tokens = tokenize(searchable_text)
    content_token_set = set(content_tokens)

    score = 0

    for token in expanded_query_tokens:
        if token in content_token_set:
            score += 3

        if token in normalize_text(title):
            score += 5

        if token in normalize_text(file_name):
            score += 5

    normalized_query = normalize_text(query)
    normalized_content = normalize_text(searchable_text)

    if normalized_query in normalized_content:
        score += 10

    return score


def retrieve_relevant_documents(query: str, top_k: int = 3) -> List[Dict]:
    documents = read_knowledge_files()

    scored_documents = []

    for document in documents:
        score = score_document(query, document)

        print(
            f"Document: {document['file_name']} | Score: {score}"
        )

        if score > 0:
            scored_documents.append(
                {
                    **document,
                    "score": score,
                    "preview": document["content"][:300].replace("\n", " "),
                }
            )

    scored_documents.sort(key=lambda item: item["score"], reverse=True)

    return scored_documents[:top_k]


def build_context_from_documents(documents: List[Dict]) -> str:
    if not documents:
        return ""

    context_parts = []

    for index, document in enumerate(documents, start=1):
        context_parts.append(
            f"""
[Document {index}]
Title: {document["title"]}
Source ID: {document["source_id"]}
File: {document["file_name"]}

Content:
{document["content"]}
"""
        )

    return "\n\n".join(context_parts)