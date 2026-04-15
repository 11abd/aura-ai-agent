import os
from app.rag.langchain_loader import load_job_documents
from app.rag.splitter import get_text_splitter
from app.rag.embedder import get_embedding_model
from app.rag.vector_store import create_vector_store, save_vector_store, load_vector_store

FAISS_PATH = os.path.join("faiss_index", "jobs_v2")


def build_or_load_vector_db():
    """
    Load existing vector DB if available,
    otherwise build and save a new one
    """

    embedding_model = get_embedding_model()

    # If index exists → load
    if os.path.exists(FAISS_PATH):
        print("Loading existing vector DB...")
        return load_vector_store(embedding_model, FAISS_PATH)

    # Else → create new
    print("Creating new vector DB...")

    jobs = load_job_documents("data/raw/jobs.txt")

    splitter = get_text_splitter()
    documents = splitter.split_documents(jobs)
    for chunk_index, document in enumerate(documents):
        document.metadata["chunk_id"] = chunk_index

    vector_store = create_vector_store(documents, embedding_model)

    # Save for future use
    save_vector_store(vector_store, FAISS_PATH)

    return vector_store
