def get_retriever(vector_store):
    """
    Convert vector store into retriever
    """
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )