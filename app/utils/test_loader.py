from app.rag.loader import load_jobs, load_resume
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_loader():
    jobs = load_jobs("data/raw/jobs.txt")
    resume = load_resume("data/raw/resume.txt")

    logger.info(f"Loaded {len(jobs)} job descriptions")

    print("\n--- SAMPLE JOB ---\n")
    print(jobs[0][:300])

    print("\n--- RESUME ---\n")
    print(resume[:300])


if __name__ == "__main__":
    test_loader()