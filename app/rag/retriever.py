import re
from collections import defaultdict


class HybridRetriever:
    """
    Blend dense retrieval with lightweight lexical and metadata reranking.
    """

    def __init__(self, vector_store, k: int = 4, fetch_k: int = 12):
        self.vector_store = vector_store
        self.k = k
        self.fetch_k = fetch_k

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9\+\#\.]+", text.lower()))

    def _score_document(self, query_tokens: set[str], doc, vector_distance: float) -> float:
        content_tokens = self._tokenize(doc.page_content)
        lexical_overlap = len(query_tokens & content_tokens) / max(len(query_tokens), 1)

        title_tokens = self._tokenize(doc.metadata.get("title", ""))
        location_tokens = self._tokenize(doc.metadata.get("location", ""))
        skill_tokens = self._tokenize(" ".join(doc.metadata.get("skills", [])))

        title_overlap = len(query_tokens & title_tokens) / max(len(title_tokens), 1)
        location_overlap = 1.0 if query_tokens & location_tokens else 0.0
        skill_overlap = len(query_tokens & skill_tokens) / max(len(skill_tokens), 1)

        semantic_score = 1 / (1 + float(vector_distance))

        return (
            semantic_score * 0.55
            + lexical_overlap * 0.25
            + title_overlap * 0.10
            + skill_overlap * 0.07
            + location_overlap * 0.03
        )

    def invoke(self, query: str):
        query_tokens = self._tokenize(query)
        candidates = self.vector_store.similarity_search_with_score(query, k=self.fetch_k)
        best_by_job = defaultdict(lambda: (-1.0, None))

        for doc, distance in candidates:
            score = self._score_document(query_tokens, doc, distance)
            job_key = doc.metadata.get("job_id", doc.metadata.get("chunk_id"))

            if score > best_by_job[job_key][0]:
                best_by_job[job_key] = (score, doc)

        ranked_docs = sorted(best_by_job.values(), key=lambda item: item[0], reverse=True)
        return [doc for _, doc in ranked_docs[: self.k]]


def get_retriever(vector_store):
    """
    Return a retriever tuned for short structured job postings.
    """
    return HybridRetriever(vector_store)
