"""Core ranking pipeline — orchestrates embedding, scoring, and ranking."""

from __future__ import annotations

import logging
from pathlib import Path

import numpy as np

from candidate_ranker.config import AppConfig, ScoringWeights
from candidate_ranker.embedding import EmbeddingEngine
from candidate_ranker.io import load_candidate, load_candidates_from_dir, load_job_description
from candidate_ranker.models import Candidate, JobDescription, RankedCandidate, ScoredDimension
from candidate_ranker.scoring.behavioral import BehavioralScorer
from candidate_ranker.scoring.experience import ExperienceScorer
from candidate_ranker.scoring.semantic import SemanticScorer
from candidate_ranker.scoring.skills import SkillScorer
from candidate_ranker.scoring.title import TitleScorer

logger = logging.getLogger(__name__)


def _build_candidate_text(candidate: Candidate) -> str:
    parts = [candidate.summary]
    for exp in candidate.experience:
        parts.append(f"{exp.title} at {exp.company}: {exp.description}")
    parts.append(" ".join(candidate.skills))
    parts.append(" ".join(candidate.education))
    return " ".join(parts)


def _generate_insights(
    candidate: Candidate,
    dims: ScoredDimension,
    scorer_skills: SkillScorer,
) -> tuple[list[str], list[str]]:
    strengths: list[str] = []
    concerns: list[str] = []

    jd_skills = scorer_skills.jd_skills
    candidate_skills_lower = set(s.lower() for s in candidate.skills)

    if candidate_skills_lower:
        matched = jd_skills & candidate_skills_lower
        if matched:
            skills_list = [s.title() for s in sorted(matched)[:5]]
            strengths.append(f"Directly relevant skills: {', '.join(skills_list)}")
        missing = jd_skills - candidate_skills_lower
        if missing:
            missing_list = [s.title() for s in sorted(missing)[:5]]
            if missing_list:
                concerns.append(f"Potential gaps: {', '.join(missing_list)}")

    if dims.semantic_similarity > 0.65:
        strengths.append("Strong semantic alignment with job requirements")
    elif dims.semantic_similarity < 0.30:
        concerns.append("Weak overall profile alignment with the role")

    if dims.behavioral_signals > 0.5:
        strengths.append("Strong behavioral signals and platform engagement")

    exp_count = len(candidate.experience)
    if exp_count >= 3:
        strengths.append(f"Substantial experience across {exp_count} roles")
    elif exp_count <= 1:
        concerns.append("Limited professional experience")

    return strengths, concerns


class RankingPipeline:
    """End-to-end candidate ranking pipeline."""

    def __init__(
        self,
        config: AppConfig | None = None,
        embedder: EmbeddingEngine | None = None,
    ) -> None:
        self.config = config or AppConfig()
        self.embedder = embedder or EmbeddingEngine(self.config.embedding)
        self.weights: ScoringWeights = self.config.scoring

    def rank(
        self,
        jd: JobDescription,
        candidates: list[Candidate],
        top_n: int | None = None,
    ) -> list[RankedCandidate]:
        top_n = top_n or self.config.pipeline.top_n
        min_threshold = self.config.pipeline.min_score_threshold
        jd_text = f"{jd.title}. {jd.description}"

        logger.info("Ranking %d candidates for: %s", len(candidates), jd.title)
        jd_embedding = self.embedder.embed(jd_text)

        # Build scorers
        semantic = SemanticScorer(jd_text, jd_embedding)
        skill = SkillScorer(jd_text, jd_embedding)
        experience = ExperienceScorer(jd_text, jd_embedding)
        title = TitleScorer(jd_text, jd_embedding)
        behavioral = BehavioralScorer(jd_text, jd_embedding)

        # Batch embed all candidates
        candidate_texts = [_build_candidate_text(c) for c in candidates]
        candidate_embeddings = self.embedder.embed_many(candidate_texts)

        scored: list[RankedCandidate] = []
        for idx, candidate in enumerate(candidates):
            emb = candidate_embeddings[idx]

            dims = ScoredDimension(
                semantic_similarity=semantic.score(candidate, emb),
                skill_match=skill.score(candidate, emb),
                experience_relevance=experience.score(candidate, emb),
                role_title_relevance=title.score(candidate, emb),
                behavioral_signals=behavioral.score(candidate, emb),
            )

            overall = (
                dims.semantic_similarity * self.weights.semantic_similarity
                + dims.skill_match * self.weights.skill_match
                + dims.experience_relevance * self.weights.experience_relevance
                + dims.role_title_relevance * self.weights.role_title_relevance
                + dims.behavioral_signals * self.weights.behavioral_signals
            )

            if overall < min_threshold:
                continue

            strengths, concerns = _generate_insights(candidate, dims, skill)

            scored.append(RankedCandidate(
                rank=0,
                candidate_id=candidate.id,
                name=candidate.name,
                overall_score=round(overall * 100, 2),
                semantic_similarity=round(dims.semantic_similarity * 100, 2),
                skill_match=round(dims.skill_match * 100, 2),
                experience_relevance=round(dims.experience_relevance * 100, 2),
                role_title_relevance=round(dims.role_title_relevance * 100, 2),
                behavioral_signals=round(dims.behavioral_signals * 100, 2),
                strengths=strengths,
                concerns=concerns,
            ))

        scored.sort(key=lambda x: x.overall_score, reverse=True)
        for i, rc in enumerate(scored, 1):
            rc.rank = i

        logger.info("Ranking complete. Top candidate: %s (%.2f)", scored[0].name, scored[0].overall_score)
        return scored[:top_n]

    def rank_from_paths(
        self,
        jd_path: str | Path,
        candidates_dir: str | Path,
        top_n: int | None = None,
    ) -> list[RankedCandidate]:
        jd = load_job_description(jd_path)
        candidates = load_candidates_from_dir(candidates_dir)
        return self.rank(jd, candidates, top_n)
