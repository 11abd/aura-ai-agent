from pathlib import Path

from app.rag.loader import RAW_DATA_DIR, RESUME_PDF_PATH, RESUME_TEXT_PATH, load_resume
from app.rag.pipeline import rebuild_vector_db
from app.utils.run_logger import RunLogger


def _clear_existing_resume_sources():
    for path in (RESUME_TEXT_PATH, RESUME_PDF_PATH):
        if path.exists():
            path.unlink()


def save_uploaded_resume(filename: str, content: bytes) -> str:
    """
    Save an uploaded resume source into data/raw.
    """
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        destination = RESUME_PDF_PATH
        destination.write_bytes(content)
    elif suffix in {".txt", ".md"}:
        destination = RESUME_TEXT_PATH
        destination.write_text(content.decode("utf-8"), encoding="utf-8")
    else:
        raise ValueError("Unsupported resume type. Use txt, md, or pdf.")

    return str(destination)


def update_resume_and_refresh_index(filename: str, content: bytes) -> dict:
    """
    Save a new resume source, parse it, and rebuild the vector DB.
    """
    logger = RunLogger()
    _clear_existing_resume_sources()
    saved_path = save_uploaded_resume(filename, content)
    parsed_resume = load_resume(saved_path)

    logger.log(
        "resume_upload",
        {
            "saved_path": saved_path,
            "filename": filename,
            "parsed_length": len(parsed_resume),
        }
    )
    logger.save_artifact("uploaded_resume_source_name", saved_path, "txt")
    logger.save_artifact("parsed_resume", parsed_resume, "md")

    rebuild_vector_db()

    logger.log("index_refresh", {"status": "rebuilt"})
    logger.save()

    return {
        "message": "Resume saved and vector index refreshed.",
        "saved_path": saved_path,
        "parsed_resume": parsed_resume,
        "run_dir": logger.run_dir,
    }
