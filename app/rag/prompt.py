from langchain_core.prompts  import PromptTemplate

def get_rag_prompt():
    """
    Prompt template for RAG-based Q&A
    """

    template = """
You are an AI job assistant.

Use the following job descriptions to answer the user's query.

Context:
{context}

User Query:
{question}

Instructions:
- Be precise and relevant
- Suggest best matching jobs
- Mention skills required
- Keep answer structured

Answer:
"""

    return PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )