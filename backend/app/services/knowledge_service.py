from pathlib import Path
from typing import List, Dict
import re


BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"


def ensure_knowledge_dir_exists():
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_file_name(file_name: str) -> str:
    file_name = file_name.strip().lower()

    file_name = re.sub(r"[^a-z0-9\-_\.]", "-", file_name)
    file_name = re.sub(r"-+", "-", file_name)

    if not file_name.endswith(".md"):
        file_name += ".md"

    if file_name.startswith("."):
        raise ValueError("Invalid file name.")

    if "/" in file_name or "\\" in file_name:
        raise ValueError("File name must not contain path separators.")

    return file_name


def extract_metadata_value(content: str, key: str, fallback: str = "unknown") -> str:
    expected_prefix = f"{key.lower()}:"

    for line in content.splitlines():
        clean_line = line.strip()

        if clean_line.lower().startswith(expected_prefix):
            return clean_line.split(":", 1)[1].strip()

    return fallback


def extract_title(content: str, fallback: str) -> str:
    for line in content.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "").strip()

    return fallback


def list_knowledge_files() -> List[Dict]:
    ensure_knowledge_dir_exists()

    files = []

    for file_path in sorted(KNOWLEDGE_DIR.glob("*.md")):
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

        version = extract_metadata_value(
            content=content,
            key="Version",
            fallback="internal-demo",
        )

        files.append(
            {
                "file_name": file_path.name,
                "title": title,
                "source_id": source_id,
                "category": category,
                "topic": topic,
                "version": version,
                "size": file_path.stat().st_size,
            }
        )

    return files


def build_markdown_document(
    title: str,
    source_id: str,
    category: str,
    topic: str,
    version: str,
    tags: str,
    content: str,
) -> str:
    return f"""# {title}

Source ID: {source_id}
Category: {category}
Topic: {topic}
Game: Honkai: Star Rail
Version: {version}
Tags: {tags}

{content.strip()}
"""


def create_knowledge_file(
    file_name: str,
    title: str,
    source_id: str,
    category: str,
    topic: str,
    version: str,
    tags: str,
    content: str,
) -> Dict:
    ensure_knowledge_dir_exists()

    safe_file_name = sanitize_file_name(file_name)
    file_path = KNOWLEDGE_DIR / safe_file_name

    if file_path.exists():
        raise ValueError(f"Knowledge file already exists: {safe_file_name}")

    markdown = build_markdown_document(
        title=title,
        source_id=source_id,
        category=category,
        topic=topic,
        version=version,
        tags=tags,
        content=content,
    )

    file_path.write_text(markdown, encoding="utf-8")

    return {
        "file_name": safe_file_name,
    }


def delete_knowledge_file(file_name: str) -> Dict:
    ensure_knowledge_dir_exists()

    safe_file_name = sanitize_file_name(file_name)
    file_path = KNOWLEDGE_DIR / safe_file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {safe_file_name}")

    file_path.unlink()

    return {
        "file_name": safe_file_name,
    }