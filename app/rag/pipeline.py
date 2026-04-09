from app.rag.loader import load_jobs
from app.rag.splitter import get_text_splitter
from app.rag.embedder import get_embedding_model
from app.rag.vector_store import create_vector_store


def build_vector_db():
    """
    Full pipeline:
    Load → Split → Embed → Store
    """

    # Load jobs
    jobs = load_jobs("data/raw/jobs.txt")

    # Split into chunks
    splitter = get_text_splitter()
    documents = splitter.create_documents(jobs)

    # Extract text
    texts = [doc.page_content for doc in documents]

    # Embeddings
    embedding_model = get_embedding_model()

    # Create vector store
    vector_store = create_vector_store(texts, embedding_model)

    return vector_store