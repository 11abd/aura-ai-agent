# AURA AI Agent

AURA AI Agent is a multi-agent resume tailoring system built for job-targeted resume generation.

It combines:
- `Planner Agent` to understand the user goal
- `Research Agent` to gather internal or external job context
- `Generator Agent` to produce a tailored resume in Markdown
- `Critic Agent` to evaluate the result using an LLM-as-judge scoring rubric
- `RAG Pipeline` to index local job data and the candidate resume
- `Run Logging` to save every run inside the `logs/` folder

## Features

- Tailors a resume to a specific job query or role target
- Uses local retrieval over stored jobs and the saved resume
- Falls back to web search when local retrieval is weak or outdated
- Produces Markdown resume output
- Scores the generated resume with a structured judge rubric
- Retries generation when the score is too low
- Saves run logs and text artifacts for research, resume drafts, and critic output
- Includes both a `FastAPI` backend and a `Streamlit` UI
- Lets you upload a new resume from the UI and rebuild the vector index at runtime

## Project Structure

```text
aura-ai-agent/
├── app/
│   ├── agents/        # Planner, research, generator, critic, prompts, schemas
│   ├── api/           # FastAPI routes and service layer
│   ├── config/        # Settings and LLM configuration
│   ├── graph/         # LangGraph workflow
│   ├── rag/           # Loading, chunking, embedding, vector store, runtime refresh
│   ├── tools/         # RAG and web-search tool wrappers
│   └── utils/         # Logging helpers
├── data/
│   └── raw/
│       ├── jobs.txt
│       └── resume.txt
├── faiss_index/       # Local vector index
├── logs/              # Per-run logs and artifacts
├── main.py            # FastAPI entrypoint
└── streamlit_app.py   # Streamlit UI
```

## How It Works

1. A user enters a job target or request.
2. The planner creates a short execution plan.
3. The research agent selects `rag` or `web_search`.
4. The generator creates a Markdown resume tailored to the retrieved context.
5. The critic evaluates the result with rubric scores and an overall score.
6. If the score is low, the system retries generation using critic feedback.
7. The system writes structured logs and artifacts into `logs/run_<timestamp>/`.

## Requirements

- Python 3.10+
- OpenAI API key
- Tavily API key for live web search

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
TAVILY_API_KEY=your_tavily_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/aura_db
```

## Installation

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run With FastAPI

Start the API server:

```bash
uvicorn main:app --reload
```

Open:

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`

### FastAPI Demo: Run The Agent

`POST /run-agent`

Example request:

```json
{
  "query": "Find machine learning roles in Chennai and tailor my resume for Python, AWS, and MLOps."
}
```

Example `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/run-agent" ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Find machine learning roles in Chennai and tailor my resume for Python, AWS, and MLOps.\"}"
```

Example response:

```json
{
  "query": "Find machine learning roles in Chennai and tailor my resume for Python, AWS, and MLOps.",
  "final_resume": "# Abdul Rahaman S\n...",
  "score": 8,
  "feedback": "Strong role fit with a few opportunities to sharpen keyword alignment.",
  "retries": 1,
  "run_dir": "logs/run_20260416_020459"
}
```

### FastAPI Demo: Upload Resume And Refresh Index

`POST /upload-resume`

Example request:

```json
{
  "resume_text": "Your latest resume text here"
}
```

Example `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/upload-resume" ^
  -H "Content-Type: application/json" ^
  -d "{\"resume_text\":\"Your latest resume text here\"}"
```

This endpoint:
- saves the resume to `data/raw/resume.txt`
- rebuilds the FAISS index immediately
- logs the upload and refresh action inside `logs/`

## Run With Streamlit

Start the UI:

```bash
streamlit run streamlit_app.py
```

Open:

- Streamlit UI: `http://localhost:8501`

### Streamlit Demo Flow

1. Open the `Knowledge Base` tab.
2. Upload a `.txt` or `.md` resume file, or paste resume text.
3. Click `Save Resume And Refresh Index`.
4. AURA saves the resume to `data/raw/resume.txt` and rebuilds the vector index during runtime.
5. Switch to the `Run Agent` tab.
6. Enter a target job request.
7. Click `Run AURA`.
8. View the generated Markdown resume, judge feedback, score, retries, and log folder path.

## Runtime Index Refresh

AURA automatically checks whether the vector index is stale based on the modification time of:

- `data/raw/jobs.txt`
- `data/raw/resume.txt`

If either file changes, the index is rebuilt at runtime when needed.

Manual refresh also happens when:

- a new resume is uploaded through Streamlit
- a new resume is uploaded through the FastAPI upload endpoint

## Logs

Every run is logged under `logs/`.

Agent runs now create a folder like:

```text
logs/run_20260416_020459/
├── run.json
├── research_context.md
├── generated_resume_attempt_1.md
├── critic_evaluation_attempt_1.md
├── final_resume.md
└── final_feedback.md
```

Resume upload and index refresh actions also create their own log folders.

## Notes

- The FAISS index is stored locally under `faiss_index/jobs_v2/`.
- The retrieval pipeline indexes both local job data and the saved resume.
- The generator always reads the latest saved `data/raw/resume.txt` at runtime.
- If the embedding model is not already cached locally, the first build may require internet access depending on your environment.

## Future Improvements

- PDF and DOCX resume ingestion
- Job upload UI alongside resume upload
- Better ranking and metadata filtering
- Persistent memory/database-backed run history
- Export final resume as PDF

## License

This project is currently for personal and portfolio use unless you add your own license.