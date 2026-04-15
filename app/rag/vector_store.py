from langchain_community.vectorstores import FAISS

def create_vector_store(documents, embedding_model):
    """
    Create FAISS vector store from documents
    """
    return FAISS.from_documents(documents, embedding_model)


def save_vector_store(vector_store, path="faiss_index"):
    """
    Save FAISS index locally
    """
    vector_store.save_local(path)


def load_vector_store(embedding_model, path="faiss_index"):
    """
    Load FAISS index from disk
    """
    return FAISS.load_local(path, embedding_model, allow_dangerous_deserialization=True)
