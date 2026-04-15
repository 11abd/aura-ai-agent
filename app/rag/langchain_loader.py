from langchain_core.documents import Document

from app.rag.loader import load_jobs, load_resume, parse_job


def load_job_documents(file_path: str):
    """
    Convert raw jobs into structured LangChain Documents.
    """
    jobs = load_jobs(file_path)

    documents = []
    for i, job in enumerate(jobs):
        parsed_job = parse_job(job)
        content = "\n".join(
            [
                f"Job Title: {parsed_job['title']}",
                f"Location: {parsed_job['location']}",
                f"Skills: {', '.join(parsed_job['skills'])}",
                f"Description: {parsed_job['description']}",
            ]
        ).strip()

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "type": "job",
                    "job_id": i,
                    "title": parsed_job["title"],
                    "location": parsed_job["location"],
                    "skills": parsed_job["skills"],
                },
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
