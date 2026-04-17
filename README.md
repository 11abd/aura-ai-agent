# AURA AI Agent

AURA AI Agent is a multi-agent resume tailoring system that helps a candidate:

- understand a target job query
- gather relevant internal or external job context
- generate a tailored resume in Markdown
- evaluate the output with an LLM-as-judge critic
- retry weak generations using structured feedback

The project combines `FastAPI`, `Streamlit`, `LangGraph`, `LangChain`, local `FAISS` retrieval, and structured run logging.

## Highlights

- Multi-agent workflow built with LangGraph
- Resume generation in Markdown
- LLM-as-judge evaluation with rubric-based scoring
- Retrieval over local job data plus the saved resume
- Web-search fallback when local retrieval is weak
- Runtime resume upload and vector index refresh
- Streamlit frontend and FastAPI backend
- Per-run logging in the `logs/` folder

## Project Flow

1. The user submits a job goal or targeting query.
2. The `Planner Agent` turns the request into a short execution plan.
3. The `Research Agent` chooses either:
   - local `RAG`
   - external `web_search`
4. The `Generator Agent` creates a tailored resume in Markdown.
5. The `Critic Agent` scores the output as an LLM judge.
6. If the score is below the retry threshold, the generator runs again with critic feedback.
7. Final artifacts and structured logs are saved under `logs/run_<timestamp>/`.

For a visual architecture graph, see [ARCHITECTURE.md](./ARCHITECTURE.md).

## Tech Stack

- `FastAPI` for backend APIs
- `Streamlit` for the frontend UI
- `LangGraph` for orchestration
- `LangChain` for prompts, loaders, and retrieval utilities
- `FAISS` for local vector search
- `OpenAI` for generation and judging
- `Tavily` for live web search fallback

## Repository Structure

```text
aura-ai-agent/
|-- app/
|   |-- agents/        # Planner, research, generator, critic, prompts, schemas
|   |-- api/           # FastAPI routes, schemas, and service layer
|   |-- config/        # Settings and LLM configuration
|   |-- graph/         # LangGraph builder, nodes, edges, state
|   |-- memory/        # Simple memory storage
|   |-- rag/           # Loaders, chunking, embedding, vector store, refresh logic
|   |-- tools/         # RAG and web-search tools
|   `-- utils/         # Logging and local test helpers
|-- data/
|   `-- raw/
|       |-- jobs.txt
|       |-- resume.txt
|       `-- resume.pdf
|-- faiss_index/       # Local FAISS index
|-- logs/              # Run logs and generated artifacts
|-- main.py            # FastAPI entrypoint
|-- streamlit_app.py   # Streamlit frontend
`-- README.md
```

## Requirements

- Python 3.10+
- OpenAI API key
- Tavily API key for live search

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini
TAVILY_API_KEY=your_tavily_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/aura_db
```

## Installation

Create and activate a virtual environment:

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

## Run the FastAPI Backend

Start the backend:

```bash
uvicorn main:app --reload
```

Available endpoints:

- Root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`

### Run the Agent

`POST /run-agent`

Example request:

```json
{
  "query": "Find machine learning roles in Chennai and tailor my resume for Python, AWS, and MLOps."
}
```

Example response:

```json
{
  "query": "Find machine learning roles in Chennai and tailor my resume for Python, AWS, and MLOps.",
  "final_resume": "# Abdul Rahaman S\n...",
  "score": 8,
  "feedback": "Strong role fit with a few improvements still needed.",
  "retries": 1,
  "run_dir": "logs/run_20260418_123456"
}
```

### Upload a Resume Source

`POST /upload-resume`

Supported formats:

- `.txt`
- `.md`
- `.pdf`

The backend parses the uploaded resume, saves it into `data/raw/`, rebuilds the vector index, and logs the refresh action.

## Run the Streamlit Frontend

Start the UI:

```bash
streamlit run streamlit_app.py
```

Open:

- `http://localhost:8501`

### Streamlit UI Flow

`Run Agent` tab:

- enter a target role or job query
- run the planner, research, generator, and critic flow
- inspect the final Markdown resume and judge feedback

`Manage Resume` tab:

- upload a `.txt`, `.md`, or `.pdf` resume
- parse the file using LangChain loaders
- rebuild the vector index immediately
- preview the parsed resume content

## Retrieval and Resume Ingestion

The RAG pipeline indexes:

- local job descriptions from `data/raw/jobs.txt`
- the active resume source from `data/raw/resume.txt` or `data/raw/resume.pdf`

Resume ingestion uses LangChain loaders:

- `TextLoader` for `.txt` and `.md`
- `PyPDFLoader` for `.pdf`

The vector index is rebuilt when:

- no index exists yet
- the source files change
- a new resume is uploaded from Streamlit or FastAPI

## Logging

Every agent run writes to a dedicated folder:

```text
logs/run_20260418_123456/
|-- run.json
|-- research_context.md
|-- generated_resume_attempt_1.md
|-- critic_evaluation_attempt_1.md
|-- final_resume.md
`-- final_feedback.md
```

Resume uploads and index refresh operations also create log folders with parsed resume artifacts.

## Current Retry Logic

The graph retries generation when:

- `score < 7`
- `retries < 5`

This means the `Critic Agent` can send the flow back to the `Generator Agent` multiple times before the graph ends.

## Notes

- The local FAISS index is stored under `faiss_index/jobs_v2/`.
- The generator uses the latest saved resume source at runtime.
- The retrieval pipeline blends vector similarity with lightweight lexical and metadata reranking.
- The first embedding build may require model download access if the embedding model is not already cached locally.

## Next Improvements

- DOCX resume parsing
- Job upload UI
- Better source attribution in research output
- Export resume to PDF
- Persistent database-backed run history
