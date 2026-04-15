from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_splitter():
    """
    Creates a text splitter for chunking documents
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", ", ", " "],
    )
