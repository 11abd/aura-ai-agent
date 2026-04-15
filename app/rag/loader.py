import os
from typing import Dict, List

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
    Load and split job descriptions
    """
    raw_text = load_text_file(file_path)
    return split_jobs(raw_text)


def load_resume(file_path: str) -> str:
    """
    Load resume text
    """
    return load_text_file(file_path)
