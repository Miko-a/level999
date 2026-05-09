from pathlib import Path
from typing import List, Dict

from app.services.vector_store_service import reset_collection


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "").strip()

    return fallback


def extract_metadata_value(content: str, key: str, fallback: str = "unknown") -> str:
    expected_prefix = f"{key.lower()}:"

    for line in content.splitlines():
        clean_line = line.strip()

        if clean_line.lower().startswith(expected_prefix):
            return clean_line.split(":", 1)[1].strip()

    return fallback


def split_markdown_into_chunks(
    content: str,
    chunk_size: int = 900,
    chunk_overlap: int = 150,
) -> List[str]:
    paragraphs = [
        paragraph.strip()
        for paragraph in content.split("\n\n")
        if paragraph.strip()
    ]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
            if current_chunk:
                current_chunk += "\n\n" + paragraph
            else:
                current_chunk = paragraph
        else:
            if current_chunk:
                chunks.append(current_chunk)

            if len(paragraph) > chunk_size:
                start = 0

                while start < len(paragraph):
                    end = start + chunk_size
                    chunk = paragraph[start:end].strip()

                    if chunk:
                        chunks.append(chunk)

                    start = end - chunk_overlap
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def load_markdown_documents() -> List[Dict]:
    documents = []

    if not KNOWLEDGE_DIR.exists():
        raise RuntimeError(f"Knowledge directory not found: {KNOWLEDGE_DIR}")

    for file_path in KNOWLEDGE_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        title = extract_title(
            content=content,
            fallback=file_path.stem.replace("-", " ").title(),
        )

        source_id = extract_metadata_value(
            content=content,
            key="Source ID",
            fallback=file_path.stem,
        )

        category = extract_metadata_value(
            content=content,
            key="Category",
            fallback="general",
        )

        topic = extract_metadata_value(
            content=content,
            key="Topic",
            fallback=file_path.stem.replace("-", " "),
        )

        game = extract_metadata_value(
            content=content,
            key="Game",
            fallback="Honkai: Star Rail",
        )

        version = extract_metadata_value(
            content=content,
            key="Version",
            fallback="internal-demo",
        )

        tags = extract_metadata_value(
            content=content,
            key="Tags",
            fallback="",
        )

        chunks = split_markdown_into_chunks(content)

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"{file_path.stem}-{chunk_index}"

            documents.append(
                {
                    "id": chunk_id,
                    "content": chunk,
                    "metadata": {
                        "title": title,
                        "source_id": source_id,
                        "file_name": file_path.name,
                        "chunk_id": chunk_id,
                        "category": category,
                        "topic": topic,
                        "game": game,
                        "version": version,
                        "tags": tags,
                    },
                }
            )

    return documents


def main():
    documents = load_markdown_documents()

    collection = reset_collection()

    if not documents:
        print("No documents found.")
        return

    collection.add(
        ids=[document["id"] for document in documents],
        documents=[document["content"] for document in documents],
        metadatas=[document["metadata"] for document in documents],
    )

    print(f"Ingested {len(documents)} chunks into Chroma collection.")

    for document in documents:
        metadata = document["metadata"]
        print(
            f"- {metadata['chunk_id']} | "
            f"{metadata['category']} | "
            f"{metadata['topic']} | "
            f"{metadata['file_name']}"
        )


if __name__ == "__main__":
    main()