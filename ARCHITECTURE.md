# AURA Architecture

This document describes the system flow of AURA AI Agent and mirrors the LangGraph execution path used by the project.

## High-Level View

AURA has three major layers:

1. Interface layer
   - `FastAPI`
   - `Streamlit`
2. Orchestration layer
   - `LangGraph`
   - planner, research, generator, critic nodes
3. Knowledge and execution layer
   - local RAG over jobs + resume
   - OpenAI LLM calls
   - Tavily web search fallback
   - run logging

## LangGraph-Style Flow

```mermaid
flowchart TD
    A[User Query] --> B[Planner Node]
    B --> C[Research Node]
    C --> D[Generator Node]
    D --> E[Critic Node]
    E -->|score < 7 and retries < 5| D
    E -->|score >= 7 or retry limit reached| F[Final Output]
```

## Expanded Execution Graph

```mermaid
flowchart TD
    U[User / API / Streamlit] --> S[AgentService.run]
    S --> G[LangGraph Compiler Graph]

    G --> P[Planner Agent]
    P --> R[Research Agent]

    R --> T{Tool Selector}
    T -->|rag| RG[RAG Tool]
    T -->|web_search| WS[Web Search Tool]

    RG --> KB[(Jobs + Resume Knowledge Base)]
    KB --> VS[FAISS Vector Store]
    VS --> RR[Hybrid Retriever]
    RR --> RC[Research Context]

    WS --> RC
    RC --> GN[Generator Agent]
    GN --> CR[Critic Agent]

    CR --> J[LLM-as-Judge Scores]
    J -->|retry| GN
    J -->|accept| O[Final Resume + Feedback]

    O --> L[Run Logger]
    RC --> L
    GN --> L
    CR --> L
```

## Runtime Resume Ingestion Flow

```mermaid
flowchart TD
    A[Resume Upload] --> B{File Type}
    B -->|txt / md| C[TextLoader]
    B -->|pdf| D[PyPDFLoader]
    C --> E[Parsed Resume Text]
    D --> E
    E --> F[Save to data/raw]
    F --> G[Rebuild Vector Index]
    G --> H[Resume + Jobs Embedded]
    H --> I[FAISS Saved to faiss_index/jobs_v2]
    I --> J[Upload Log Saved in logs/]
```

## Node Responsibilities

### Planner Node

- input: user query
- output: short execution plan
- purpose: shape the downstream work

### Research Node

- input: user query
- output: grounded job context
- purpose: choose between local retrieval and web search

### Generator Node

- input: research context + optional critic feedback
- output: tailored Markdown resume
- purpose: generate a stronger, role-targeted resume draft

### Critic Node

- input: context + generated resume
- output: score, verdict, feedback, rubric fields
- purpose: judge resume quality and decide whether to retry

## Retry Logic

Implemented in `app/graph/edges.py`:

```python
if score < 7 and retries < 5:
    return "retry"
return "end"
```

That creates a feedback loop:

```text
Generator -> Critic -> Generator -> Critic -> ... -> End
```

## Data Flow

### Inputs

- job descriptions from `data/raw/jobs.txt`
- resume source from `data/raw/resume.txt` or `data/raw/resume.pdf`
- user query from FastAPI or Streamlit

### Intermediate Data

- execution plan
- research context
- generated resume drafts
- critic evaluations

### Outputs

- final Markdown resume
- judge feedback and score
- run artifacts in `logs/run_<timestamp>/`

## Logging Flow

Each run produces:

- structured `run.json`
- research context artifact
- generated resume attempt artifacts
- critic evaluation attempt artifacts
- final resume and final feedback artifacts

This makes the graph behavior auditable step by step.

## Files to Know

- [app/graph/builder.py](C:/Users/abdus/Documents/aura-ai-agent/app/graph/builder.py)
- [app/graph/edges.py](C:/Users/abdus/Documents/aura-ai-agent/app/graph/edges.py)
- [app/graph/nodes.py](C:/Users/abdus/Documents/aura-ai-agent/app/graph/nodes.py)
- [app/rag/pipeline.py](C:/Users/abdus/Documents/aura-ai-agent/app/rag/pipeline.py)
- [app/rag/loader.py](C:/Users/abdus/Documents/aura-ai-agent/app/rag/loader.py)
- [app/api/service.py](C:/Users/abdus/Documents/aura-ai-agent/app/api/service.py)
- [streamlit_app.py](C:/Users/abdus/Documents/aura-ai-agent/streamlit_app.py)
