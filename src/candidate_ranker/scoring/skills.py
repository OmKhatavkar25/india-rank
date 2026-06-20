from candidate_ranker.models import Candidate
from candidate_ranker.scoring import BaseScorer
from candidate_ranker.skills import extract_skills, skill_coverage


class SkillScorer(BaseScorer):
    """Fraction of JD-required skills present in candidate profile."""

    def __init__(self, jd_text: str, *args, **kwargs) -> None:
        super().__init__(jd_text, *args, **kwargs)
        self._jd_skills: set[str] = set(extract_skills(jd_text))

    @property
    def jd_skills(self) -> set[str]:
        return self._jd_skills

    def score(self, candidate: Candidate, candidate_embedding: ...) -> float:
        candidate_text = " ".join([
            candidate.summary,
            " ".join(s.lower() for s in candidate.skills),
            " ".join(e.title + " " + e.description for e in candidate.experience),
        ])
        candidate_skills = set(extract_skills(candidate_text))
        return skill_coverage(self._jd_skills, candidate_skills)
