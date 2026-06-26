from __future__ import annotations

import logging
import os
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

from candidate_ranker.redrob_models import Candidate

logger = logging.getLogger("semantic")

JD_TEXT = (
    "Senior AI Engineer \u2014 Founding Team at Redrob AI. "
    "Build scalable AI systems including recommendation engines, ranking algorithms, "
    "retrieval augmented generation (RAG) pipelines, and vector-based search. "
    "Work with embeddings, vector databases (Pinecone, Weaviate, Qdrant, Milvus, FAISS), "
    "and evaluation metrics (NDCG, MRR, MAP). Fine-tune LLMs using LoRA/QLoRA/PEFT. "
    "Deploy production ML systems at scale. Python expertise required. "
    "Startup or early-stage experience valued. Based in Pune or Noida preferred."
)


def _candidate_text(candidate: Candidate) -> str:
    parts = []
    if candidate.profile.headline:
        parts.append(candidate.profile.headline)
    if candidate.profile.summary:
        parts.append(candidate.profile.summary)
    if candidate.skills:
        names = [s.name for s in candidate.skills[:50]]
        parts.append(f"Skills: {', '.join(names)}")
    # Include up to 5 most-recent career descriptions — catches ML work
    # at companies where the title isn't ML-tagged.
    descs = []
    for entry in candidate.career_history:
        if entry.description and len(entry.description) > 15:
            descs.append(entry.description)
        if len(descs) >= 5:
            break
    if descs:
        parts.append("Experience: " + " | ".join(descs))
    return ". ".join(parts)


def precompute_embeddings(
    candidates: list[Candidate],
    cache_path: Path,
    model_name: str = "all-MiniLM-L6-v2",
) -> np.ndarray:
    texts = [_candidate_text(c) for c in candidates]
    logger.info("Loading model %s ...", model_name)
    model = SentenceTransformer(model_name)
    logger.info("Encoding %d candidates ...", len(texts))
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=128)
    np.save(str(cache_path), embeddings)
    logger.info("Saved %d embeddings to %s", len(embeddings), cache_path)
    return embeddings


def _compute_from_cache(candidates, cache_path):
    logger.info("Loading embeddings from %s ...", cache_path)
    candidate_embs = np.load(str(cache_path))

    logger.info("Encoding JD text (offline mode) ...")
    os.environ["HF_HUB_OFFLINE"] = "1"
    model = SentenceTransformer("all-MiniLM-L6-v2")
    jd_emb = model.encode([JD_TEXT])[0]

    norms = np.linalg.norm(candidate_embs, axis=1, keepdims=True)
    candidate_embs = candidate_embs / np.maximum(norms, 1e-12)
    jd_norm = np.linalg.norm(jd_emb)
    jd_emb = jd_emb / max(jd_norm, 1e-12)

    return candidate_embs @ jd_emb


def _compute_tfidf_scores(candidates):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    texts = [_candidate_text(c) for c in candidates]
    all_texts = [JD_TEXT] + texts
    logger.info("Computing TF-IDF similarity for %d candidates ...", len(texts))
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    jd_vec = tfidf_matrix[0:1]
    candidate_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(jd_vec, candidate_vecs).flatten()
    return similarities


def compute_semantic_scores(
    candidates: list[Candidate],
    cache_path: Path,
) -> dict[str, float]:
    if cache_path.exists():
        similarities = _compute_from_cache(candidates, cache_path)
    else:
        logger.warning("No embedding cache found. Using TF-IDF fallback.")
        logger.warning("Run `python rank.py --precompute` once for better semantic matching.")
        similarities = _compute_tfidf_scores(candidates)

    min_sim, max_sim = float(similarities.min()), float(similarities.max())
    if max_sim > min_sim:
        normalized = (similarities - min_sim) / (max_sim - min_sim)
    else:
        normalized = np.zeros_like(similarities)

    return {
        c.candidate_id: float(normalized[i])
        for i, c in enumerate(candidates)
    }
