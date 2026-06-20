"""Integration tests for the full pipeline."""

import json
import tempfile
from pathlib import Path

from candidate_ranker.pipeline import RankingPipeline

SAMPLE_JD = {
    "title": "Senior Software Engineer",
    "description": "We need a senior engineer with Python, Go, Kubernetes, and distributed systems experience. 5+ years required.",
}

SAMPLE_CANDIDATE = {
    "name": "Alice",
    "summary": "Senior engineer with 7 years in distributed systems at Google.",
    "skills": ["Python", "Go", "Kubernetes", "Docker", "AWS"],
    "total_experience_years": 7,
    "seniority_level": "senior",
    "education": ["B.S. Computer Science"],
    "experience": [
        {"title": "Senior Software Engineer", "company": "Google", "duration_years": 5, "description": "Built large-scale distributed systems."},
        {"title": "Software Engineer", "company": "Amazon", "duration_years": 2, "description": "Worked on AWS infrastructure."},
    ],
    "behavioral_signals": {
        "open_source_contributions": 10,
        "platform_activity_level": "high",
        "leadership_experience": True,
        "publications": 2,
        "speaking_engagements": 3,
        "collaboration_score": 0.85,
    },
}


def test_pipeline_end_to_end() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)

        # Write JD
        jd_path = tmp_path / "jd.json"
        with open(jd_path, "w") as f:
            json.dump(SAMPLE_JD, f)

        # Write candidate
        cand_dir = tmp_path / "candidates"
        cand_dir.mkdir()
        with open(cand_dir / "alice.json", "w") as f:
            json.dump(SAMPLE_CANDIDATE, f)

        # Run pipeline
        pipeline = RankingPipeline()
        ranked = pipeline.rank_from_paths(jd_path, cand_dir, top_n=5)

        assert len(ranked) == 1
        assert ranked[0].name == "Alice"
        assert ranked[0].rank == 1
        assert ranked[0].overall_score > 50.0
        assert ranked[0].semantic_similarity > 0
        assert ranked[0].skill_match > 0
        assert ranked[0].experience_relevance > 0


def test_pipeline_multiple_candidates() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        jd_path = tmp_path / "jd.json"
        with open(jd_path, "w") as f:
            json.dump(SAMPLE_JD, f)

        cand_dir = tmp_path / "candidates"
        cand_dir.mkdir()

        candidates = [
            {**SAMPLE_CANDIDATE, "name": "Alice", "skills": ["Python", "Go", "Kubernetes"]},
            {**SAMPLE_CANDIDATE, "name": "Bob", "skills": ["Java", "Spring"]},
            {**SAMPLE_CANDIDATE, "name": "Carol", "skills": ["Python", "Docker", "Kubernetes", "AWS"]},
        ]
        for i, c in enumerate(candidates):
            with open(cand_dir / f"c{i}.json", "w") as f:
                json.dump(c, f)

        pipeline = RankingPipeline()
        ranked = pipeline.rank_from_paths(jd_path, cand_dir, top_n=3)

        assert len(ranked) == 3
        # Alice and Carol should rank above Bob
        assert ranked[0].overall_score >= ranked[1].overall_score >= ranked[2].overall_score
