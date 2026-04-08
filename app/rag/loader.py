import os
from typing import List

def load_text_file(file_path: str) -> str:
    """
    Load a text file and return content as string
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def split_jobs(raw_text: str) -> List[str]:
    """
    Split jobs using separator ---
    """
    jobs = raw_text.split("---")
    return [job.strip() for job in jobs if job.strip()]


def load_jobs(file_path: str) -> List[str]:
    """
    Load and split job descriptions
    """
    raw_text = load_text_file(file_path)
    return split_jobs(raw_text)


def load_resume(file_path: str) -> str:
    """
    Load resume text
    """
    return load_text_file(file_path)