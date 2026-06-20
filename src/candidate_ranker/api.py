"""FastAPI REST API for the Candidate Ranker."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel

from candidate_ranker.config import AppConfig
from candidate_ranker.embedding import EmbeddingEngine
from candidate_ranker.io import load_candidate, load_job_description
from candidate_ranker.models import Candidate
from candidate_ranker.pipeline import RankingPipeline

app = FastAPI(title="Candidate Ranker API", version="1.0.0")

_config = AppConfig()
_embedder = EmbeddingEngine(_config.embedding)
_pipeline = RankingPipeline(config=_config, embedder=_embedder)


class RankRequest(BaseModel):
    job_description: str
    job_title: str = ""
    top_n: int = 20


class RankResponse(BaseModel):
    ranked: list[dict]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/rank", response_model=RankResponse)
def rank_candidates(request: RankRequest) -> RankResponse:
    """Rank candidates against a job description sent as text."""
    if not request.job_description:
        raise HTTPException(400, "job_description is required")

    # Build JD object
    jd = load_job_description.__wrapped__ if hasattr(load_job_description, "__wrapped__") else type("JD", (), {})()
    jd.title = request.job_title or "Custom Role"
    jd.description = request.job_description

    candidates: list[Candidate] = []

    # Try loading from default data directory
    data_dir = Path("data/candidates")
    if data_dir.exists():
        from candidate_ranker.io import load_candidates_from_dir
        candidates = load_candidates_from_dir(data_dir)

    if not candidates:
        raise HTTPException(400, "No candidate data available. Upload candidates or place them in data/candidates/")

    ranked = _pipeline.rank(jd, candidates, top_n=request.top_n)
    return RankResponse(ranked=[rc.to_dict() for rc in ranked])


@app.post("/upload-candidate")
def upload_candidate(file: UploadFile) -> dict:
    """Upload a candidate JSON file."""
    content = file.file.read()
    import json
    raw = json.loads(content)
    data_dir = Path("data/candidates")
    data_dir.mkdir(parents=True, exist_ok=True)
    dest = data_dir / file.filename
    with open(dest, "wb") as f:
        f.write(content)
    return {"status": "ok", "path": str(dest), "name": raw.get("name", "unknown")}
