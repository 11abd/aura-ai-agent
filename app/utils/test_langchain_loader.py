from app.rag.langchain_loader import load_job_documents, load_resume_document
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_langchain_loader():
    job_docs = load_job_documents("data/raw/jobs.txt")
    resume_doc = load_resume_document("data/raw/resume.txt")

    logger.info(f"Loaded {len(job_docs)} job documents")

    print("\n--- JOB DOC SAMPLE ---\n")
    print(job_docs[0].page_content[:200])
    print(job_docs[0].metadata)

    print("\n--- RESUME DOC ---\n")
    print(resume_doc[0].page_content[:200])
    print(resume_doc[0].metadata)


if __name__ == "__main__":
    test_langchain_loader()