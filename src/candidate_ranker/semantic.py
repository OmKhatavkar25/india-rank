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
        parts.append(candidate.profile.summary[:800])
    if candidate.skills:
        names = [s.name for s in candidate.skills[:30]]
        parts.append(f"Skills: {', '.join(names)}")
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


def compute_semantic_scores(
    candidates: list[Candidate],
    cache_path: Path,
) -> dict[str, float]:
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

    similarities = candidate_embs @ jd_emb

    min_sim, max_sim = float(similarities.min()), float(similarities.max())
    if max_sim > min_sim:
        normalized = (similarities - min_sim) / (max_sim - min_sim)
    else:
        normalized = np.zeros_like(similarities)

    return {
        c.candidate_id: float(normalized[i])
        for i, c in enumerate(candidates)
    }
