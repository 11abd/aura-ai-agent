import json
import os
import shutil

from app.rag.embedder import get_embedding_model
from app.rag.langchain_loader import load_knowledge_documents
from app.rag.loader import JOB_FILE_PATH, resolve_resume_path
from app.rag.splitter import get_text_splitter
from app.rag.vector_store import create_vector_store, load_vector_store, save_vector_store

FAISS_PATH = os.path.join("faiss_index", "jobs_v2")
INDEX_META_PATH = os.path.join(FAISS_PATH, "index_meta.json")


def _source_metadata() -> dict:
    try:
        resume_path = resolve_resume_path()
    except FileNotFoundError:
        resume_path = None

    return {
        "job_file": {
            "path": str(JOB_FILE_PATH),
            "mtime": os.path.getmtime(JOB_FILE_PATH) if os.path.exists(JOB_FILE_PATH) else None,
        },
        "resume_file": {
            "path": resume_path,
            "mtime": os.path.getmtime(resume_path) if resume_path and os.path.exists(resume_path) else None,
        },
    }


def _load_index_metadata() -> dict:
    if not os.path.exists(INDEX_META_PATH):
        return {}

    with open(INDEX_META_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def _save_index_metadata(metadata: dict):
    os.makedirs(FAISS_PATH, exist_ok=True)
    with open(INDEX_META_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=4)


def is_vector_db_stale() -> bool:
    """
    Check whether the vector DB should be rebuilt.
    """
    if not os.path.exists(FAISS_PATH):
        return True

    return _load_index_metadata().get("sources") != _source_metadata()


def rebuild_vector_db():
    """
    Rebuild the vector DB from current job and resume sources.
    """
    embedding_model = get_embedding_model()

    if os.path.exists(FAISS_PATH):
        shutil.rmtree(FAISS_PATH)

    documents = load_knowledge_documents(str(JOB_FILE_PATH))
    splitter = get_text_splitter()
    chunks = splitter.split_documents(documents)

    for chunk_index, document in enumerate(chunks):
        document.metadata["chunk_id"] = chunk_index

    vector_store = create_vector_store(chunks, embedding_model)
    save_vector_store(vector_store, FAISS_PATH)
    _save_index_metadata(
        {
            "sources": _source_metadata(),
            "chunk_count": len(chunks),
        }
    )
    return vector_store


def build_or_load_vector_db(force_rebuild: bool = False):
    """
    Load an existing vector DB when valid, otherwise rebuild it.
    """
    embedding_model = get_embedding_model()

    if force_rebuild or is_vector_db_stale():
        return rebuild_vector_db()

    return load_vector_store(embedding_model, FAISS_PATH)
