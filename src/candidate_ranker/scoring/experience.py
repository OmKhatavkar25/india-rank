import re

import numpy as np

from candidate_ranker.models import Candidate
from candidate_ranker.scoring import BaseScorer


SENIORITY_MAP = {
    "junior": 1, "entry": 1, "graduate": 1,
    "mid": 2, "intermediate": 2,
    "senior": 3, "staff": 3,
    "lead": 4, "manager": 4,
    "principal": 5, "fellow": 5, "distinguished": 5,
}

SENIORITY_KEYWORDS = {
    "senior": 3, "lead": 4, "manager": 4, "staff": 3,
    "principal": 5, "junior": 1, "mid": 2, "entry": 1,
    "head": 5, "director": 5, "vp": 5, "chief": 5,
}


class ExperienceScorer(BaseScorer):
    """Evaluates experience years and seniority alignment."""

    def score(self, candidate: Candidate, candidate_embedding: np.ndarray) -> float:
        total_years = candidate.total_experience_years or sum(
            e.duration_years for e in candidate.experience
        )
        seniority_weight = SENIORITY_MAP.get(candidate.seniority_level.lower(), 2)
        jd_seniority = self._infer_jd_seniority()

        # Base: years of experience (cap at 15+ years = 1.0)
        years_score = min(total_years / 15.0, 1.0)

        # Seniority alignment
        if jd_seniority > 0:
            diff = abs(seniority_weight - jd_seniority)
            seniority_score = max(0.0, 1.0 - diff * 0.25)
            return years_score * 0.6 + seniority_score * 0.4

        return years_score

    def _infer_jd_seniority(self) -> int:
        """Guess required seniority level from JD text."""
        jd_lower = self.jd_text.lower()
        max_level = 0
        for word, level in SENIORITY_KEYWORDS.items():
            if re.search(rf"\b{re.escape(word)}\b", jd_lower):
                max_level = max(max_level, level)
        return max_level
