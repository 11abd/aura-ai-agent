import os
from pathlib import Path
from typing import Dict, List, Optional

from langchain_community.document_loaders import PyPDFLoader, TextLoader

RAW_DATA_DIR = Path("data") / "raw"
JOB_FILE_PATH = RAW_DATA_DIR / "jobs.txt"
RESUME_TEXT_PATH = RAW_DATA_DIR / "resume.txt"
RESUME_PDF_PATH = RAW_DATA_DIR / "resume.pdf"
SUPPORTED_RESUME_EXTENSIONS = {".txt", ".md", ".pdf"}


def _load_documents(file_path: str):
    """
    Load documents using a LangChain loader based on file type.
    """
    suffix = Path(file_path).suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)
    elif suffix in {".txt", ".md"}:
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return loader.load()


def load_document_text(file_path: str) -> str:
    """
    Load a supported file and return a single normalized text string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    documents = _load_documents(file_path)
    return "\n\n".join(doc.page_content.strip() for doc in documents if doc.page_content.strip())


def resolve_resume_path(preferred_path: Optional[str] = None) -> str:
    """
    Resolve the current resume source file.
    """
    if preferred_path:
        candidate = Path(preferred_path)
        if candidate.exists():
            return str(candidate)

    for candidate in (RESUME_PDF_PATH, RESUME_TEXT_PATH):
        if candidate.exists():
            return str(candidate)

    raise FileNotFoundError("No resume source found in data/raw. Expected resume.txt or resume.pdf")


def split_jobs(raw_text: str) -> List[str]:
    """
    Split jobs using separator ---
    """
    jobs = raw_text.split("---")
    return [job.strip() for job in jobs if job.strip()]


def parse_job(job_text: str) -> Dict[str, object]:
    """
    Extract structured job fields from a raw job posting block.
    """
    parsed = {
        "title": "",
        "location": "",
        "skills": [],
        "description": "",
    }

    description_lines = []
    in_description = False

    for raw_line in job_text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("Job Title:"):
            parsed["title"] = line.partition(":")[2].strip()
            in_description = False
            continue

        if line.startswith("Location:"):
            parsed["location"] = line.partition(":")[2].strip()
            in_description = False
            continue

        if line.startswith("Skills:"):
            skills = line.partition(":")[2].strip()
            parsed["skills"] = [skill.strip() for skill in skills.split(",") if skill.strip()]
            in_description = False
            continue

        if line.startswith("Description:"):
            in_description = True
            remainder = line.partition(":")[2].strip()
            if remainder:
                description_lines.append(remainder)
            continue

        if in_description:
            description_lines.append(line)

    parsed["description"] = "\n".join(description_lines).strip()

    return parsed


def load_jobs(file_path: str) -> List[str]:
    """
    Load and split job descriptions.
    """
    raw_text = load_document_text(file_path)
    return split_jobs(raw_text)


def load_resume(file_path: Optional[str] = None) -> str:
    """
    Load resume text from txt, md, or pdf source.
    """
    return load_document_text(resolve_resume_path(file_path))
