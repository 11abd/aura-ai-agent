from pathlib import Path

import streamlit as st

from app.api.service import AgentService
from app.config.settings import settings
from app.rag.knowledge_base import update_resume_and_refresh_index
from app.rag.loader import resolve_resume_path, load_resume
from app.rag.pipeline import is_vector_db_stale


st.set_page_config(page_title=settings.APP_NAME, page_icon="A", layout="wide")


def _current_resume_preview() -> tuple[str, str]:
    try:
        resume_path = resolve_resume_path()
        return resume_path, load_resume(resume_path)
    except FileNotFoundError:
        return "", ""


st.title(settings.APP_NAME)
st.caption("Resume tailoring with retrieval, critique, and runtime resume ingestion.")

run_tab, resume_tab = st.tabs(["Run Agent", "Manage Resume"])

with run_tab:
    st.subheader("Tailor a resume")
    query = st.text_area(
        "Target job or instruction",
        placeholder="Example: Tailor my resume for a machine learning engineer role in Chennai with Python, AWS, and MLOps requirements.",
        height=150,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("App", settings.APP_NAME)
    col2.metric("Model", settings.OPENAI_MODEL)
    col3.metric("Index", "Refresh needed" if is_vector_db_stale() else "Ready")

    if st.button("Run AURA", type="primary", use_container_width=True):
        if not query.strip():
            st.error("Enter a target job query first.")
        else:
            with st.spinner("Running planner, research, generation, and judge steps..."):
                result = AgentService().run(query.strip())

            st.success(f"Completed. Logs saved in `{result['run_dir']}`")

            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Score", f"{result['score']}/10" if result["score"] else "N/A")
            metric2.metric("Retries", result["retries"])
            metric3.metric("Log Folder", result["run_dir"])

            output_heading = "### Final Resume" if result["score"] else "### Response"
            st.markdown(output_heading)
            st.markdown(result["final_resume"])

            if result["feedback"]:
                st.markdown("### Judge Feedback")
                st.markdown(result["feedback"])

            st.download_button(
                "Download Output",
                data=result["final_resume"],
                file_name="final_resume.md",
                mime="text/markdown",
                use_container_width=True,
            )

with resume_tab:
    st.subheader("Add or replace resume source")
    st.write("Upload a `.txt`, `.md`, or `.pdf` resume. PDFs are parsed with LangChain's `PyPDFLoader` before the index is refreshed.")

    current_path, current_resume = _current_resume_preview()
    st.text_input("Current resume source", value=current_path or "No resume source saved yet", disabled=True)
    st.text_area("Current parsed resume preview", value=current_resume, height=240, disabled=True)

    uploaded_file = st.file_uploader(
        "Upload resume",
        type=["txt", "md", "pdf"],
        accept_multiple_files=False,
    )

    if st.button("Save Resume And Refresh Index", use_container_width=True):
        if uploaded_file is None:
            st.error("Upload a resume file first.")
        else:
            with st.spinner("Saving resume, parsing it, and rebuilding the vector index..."):
                result = update_resume_and_refresh_index(uploaded_file.name, uploaded_file.getvalue())

            st.success(result["message"])
            st.write(f"Saved path: `{result['saved_path']}`")
            st.write(f"Log folder: `{result['run_dir']}`")
            st.markdown("### Parsed Resume Preview")
            st.markdown(result["parsed_resume"])
            st.rerun()
