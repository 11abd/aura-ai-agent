from langchain_community.embeddings import HuggingFaceEmbeddings

def get_embedding_model():
    """
    Returns embedding model (local, free)
    """
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )