"""Data loading — reads JSON files and converts to domain models."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from candidate_ranker.models import BehavioralSignals, Candidate, Experience, JobDescription

logger = logging.getLogger(__name__)


def load_job_description(path: str | Path) -> JobDescription:
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return JobDescription(
        id=path.stem,
        title=raw.get("title", ""),
        description=raw.get("description", ""),
    )


def load_candidate(path: str | Path) -> Candidate:
    path = Path(path)
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    experience = [
        Experience(
            title=e.get("title", ""),
            company=e.get("company", ""),
            duration_years=e.get("duration_years", 0),
            description=e.get("description", ""),
        )
        for e in raw.get("experience", [])
    ]

    signals_raw = raw.get("behavioral_signals", {})
    signals = BehavioralSignals(
        open_source_contributions=signals_raw.get("open_source_contributions", 0),
        platform_activity_level=signals_raw.get("platform_activity_level", "low"),
        leadership_experience=signals_raw.get("leadership_experience", False),
        publications=signals_raw.get("publications", 0),
        speaking_engagements=signals_raw.get("speaking_engagements", 0),
        collaboration_score=signals_raw.get("collaboration_score", 0.0),
    )

    return Candidate(
        id=path.stem,
        name=raw.get("name", path.stem),
        summary=raw.get("summary", ""),
        skills=raw.get("skills", []),
        total_experience_years=raw.get("total_experience_years", 0),
        seniority_level=raw.get("seniority_level", "mid"),
        education=raw.get("education", []),
        experience=experience,
        behavioral_signals=signals,
    )


def load_candidates_from_dir(dir_path: str | Path) -> list[Candidate]:
    dir_path = Path(dir_path)
    candidates = []
    for fp in sorted(dir_path.glob("*.json")):
        try:
            candidates.append(load_candidate(fp))
        except Exception:
            logger.exception("Failed to load candidate from %s", fp)
    return candidates
