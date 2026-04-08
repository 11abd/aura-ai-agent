from langchain_loader import Document
from app.rag.loader import load_jobs, load_resume


def load_job_documents(file_path: str):
    """
    Convert job text into LangChain Documents
    """
    jobs = load_jobs(file_path)

    documents = []
    for i, job in enumerate(jobs):
        documents.append(
            Document(
                page_content=job,
                metadata={"type": "job", "id": i}
            )
        )

    return documents


def load_resume_document(file_path: str):
    """
    Convert resume into LangChain Document
    """
    resume = load_resume(file_path)

    return [
        Document(
            page_content=resume,
            metadata={"type": "resume"}
        )
    ]