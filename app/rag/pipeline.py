import os
from app.rag.loader import load_jobs
from app.rag.splitter import get_text_splitter
from app.rag.embedder import get_embedding_model
from app.rag.vector_store import create_vector_store, save_vector_store, load_vector_store

FAISS_PATH = "faiss_index"


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

    jobs = load_jobs("data/raw/jobs.txt")

    splitter = get_text_splitter()
    documents = splitter.create_documents(jobs)

    texts = [doc.page_content for doc in documents]

    vector_store = create_vector_store(texts, embedding_model)

    # Save for future use
    save_vector_store(vector_store, FAISS_PATH)

    return vector_store