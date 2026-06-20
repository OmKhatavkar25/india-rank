"""Tests for individual scoring dimensions."""

import numpy as np

from candidate_ranker.models import BehavioralSignals, Candidate, Experience
from candidate_ranker.scoring.behavioral import BehavioralScorer
from candidate_ranker.scoring.experience import ExperienceScorer
from candidate_ranker.scoring.semantic import SemanticScorer
from candidate_ranker.scoring.title import TitleScorer

JD_TEXT = "Senior Software Engineer with experience in Python, Go, Kubernetes, and distributed systems."
JD_EMB = np.zeros(384)  # dummy


def _make_candidate(**kwargs) -> Candidate:
    defaults = dict(
        id="test",
        name="Test",
        summary="A software engineer",
        skills=["Python", "Go"],
        total_experience_years=5,
        seniority_level="senior",
        education=["B.S. CS"],
        experience=[
            Experience(title="Senior Engineer", company="Acme", duration_years=3, description="Built stuff"),
            Experience(title="Engineer", company="Beta", duration_years=2, description="Built more stuff"),
        ],
        behavioral_signals=BehavioralSignals(),
    )
    defaults.update(kwargs)
    return Candidate(**defaults)


def test_semantic_scorer_returns_float() -> None:
    scorer = SemanticScorer(JD_TEXT, JD_EMB)
    cand = _make_candidate()
    score = scorer.score(cand, np.ones(384))
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_experience_scorer_years() -> None:
    scorer = ExperienceScorer(JD_TEXT, JD_EMB)
    cand = _make_candidate(total_experience_years=10)
    score = scorer.score(cand, np.ones(384))
    assert 0.0 <= score <= 1.0


def test_experience_scorer_seniority_alignment() -> None:
    """Senior engineer applying to senior role should score well."""
    scorer = ExperienceScorer("Senior Software Engineer needed. 5+ years exp.", JD_EMB)
    cand = _make_candidate(total_experience_years=8, seniority_level="senior")
    score = scorer.score(cand, np.ones(384))
    assert score > 0.5


def test_behavioral_scorer_zero() -> None:
    scorer = BehavioralScorer(JD_TEXT, JD_EMB)
    cand = _make_candidate(behavioral_signals=BehavioralSignals())
    score = scorer.score(cand, np.ones(384))
    assert score == 0.0


def test_behavioral_scorer_high() -> None:
    scorer = BehavioralScorer(JD_TEXT, JD_EMB)
    signals = BehavioralSignals(
        open_source_contributions=15,
        platform_activity_level="high",
        leadership_experience=True,
        publications=3,
        speaking_engagements=4,
        collaboration_score=0.9,
    )
    cand = _make_candidate(behavioral_signals=signals)
    score = scorer.score(cand, np.ones(384))
    assert score > 0.5
    assert score <= 1.0


def test_title_scorer_match() -> None:
    scorer = TitleScorer("Looking for a Senior Software Engineer", JD_EMB)
    cand = _make_candidate()
    score = scorer.score(cand, np.ones(384))
    assert score > 0.0


def test_title_scorer_no_match() -> None:
    scorer = TitleScorer("Looking for a Data Scientist with ML background", JD_EMB)
    cand = _make_candidate(experience=[
        Experience(title="Frontend Developer", company="Co", duration_years=2, description="UI work"),
    ])
    score = scorer.score(cand, np.ones(384))
    assert score < 1.0
