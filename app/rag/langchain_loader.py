from pathlib import Path

from langchain_core.documents import Document

from app.rag.loader import load_jobs, load_resume, parse_job, resolve_resume_path


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
                    "source_path": file_path,
                },
            )
        )

    return documents


def load_resume_document(file_path: str | None = None):
    """
    Convert resume into a LangChain Document.
    """
    resolved_path = resolve_resume_path(file_path)
    resume = load_resume(resolved_path)

    return [
        Document(
            page_content=resume,
            metadata={
                "type": "resume",
                "title": "Candidate Resume",
                "location": "",
                "skills": [],
                "source_path": resolved_path,
                "source_name": Path(resolved_path).name,
            },
        )
    ]


def load_knowledge_documents(job_file_path: str, resume_file_path: str | None = None):
    """
    Load all internal knowledge documents used by RAG.
    """
    return load_job_documents(job_file_path) + load_resume_document(resume_file_path)
